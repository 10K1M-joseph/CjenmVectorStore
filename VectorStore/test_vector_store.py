from flask import Flask, request, jsonify
from version_json import get_version_str
import logging
from flask_restx import Api, Resource, fields, reqparse
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from dotenv import load_dotenv
import psycopg2
import numpy as np
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from VectorStore.load_pinecone import retriever, extract_video_clip_ids
from VectorStore.user_to_gpt import user_input_gpt


app = Flask(__name__)
app_version = get_version_str(
    os.path.join(os.path.dirname(__file__), "version.json"), format="display"
)
api = Api(app, version=app_version, title="CJENM Video Retrieval", doc="/api/docs")

app.config.from_pyfile(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "flask_config.py")),
    silent=True,
)

load_dotenv()

# Constants
THRESHOLD = 0.2
EXPIRES_IN = 3600
host = os.environ.get("HOST")
port = os.environ.get("PORT")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
db = os.environ.get("DATABASE")
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
region = os.environ.get("REGION_NAME")
bucket = os.environ.get("BUCKET")


# init
nltk.download("punkt")


def create_connection():
    try:
        logging.info(f"try DB connection: {host}")
        # PostgreSQL 데이터베이스에 연결
        connection = psycopg2.connect(
            host=host, database=db, user=username, password=password, port=port
        )
        logging.info("Connection to PostgreSQL DB successful")
        return connection
    except psycopg2.OperationalError as e:
        logging.error(f"Error: '{e}' occurred while connecting to the database")
        return None


def generate_url(result):
    """
    코사인 유사도 결과로 나온 항목들의 프리사인 URL을 생성합니다.

    :return: 영상과 썸네일의 url이 포함된 결과 출력
    """
    try:
        # S3 클라이언트 생성
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region,
        )

        video_presigned_url = []
        thumbnail_presigned_url = []

        for i in range(len(result)):
            video_object_key = result[i]["videoName"]
            thumbnail_object_key = result[i]["thumbnailName"]

            # presigned_url 생성
            video_url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket,
                    "Key": video_object_key,
                },  # 'ResponseContentDisposition': 'inline', "ResponseContentType": "video/mp4"},
                ExpiresIn=EXPIRES_IN,
            )

            thumbnail_url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket,
                    "Key": thumbnail_object_key,
                },  #'ResponseContentDisposition': 'inline', "ResponseContentType": "image/png"},
                ExpiresIn=EXPIRES_IN,
            )

            video_presigned_url.append(video_url)
            thumbnail_presigned_url.append(thumbnail_url)

        return video_presigned_url, thumbnail_presigned_url
    except NoCredentialsError:
        logging.error("AWS 자격 증명이 제공되지 않았습니다.")
        return None, None

    except PartialCredentialsError:
        logging.error("자격 증명 정보가 불완전합니다.")
        return None, None

    except Exception as e:
        logging.error(f"오류가 발생했습니다: {e}")
        return None, None


# 검색어와 클립의 텍스트를 결합하여 벡터화하고 유사도 계산


def search_clips(search_text, summary_datas, cursor):
    try:
        users_input = user_input_gpt(user_input=search_text)
        print("gpt대답", users_input)
        vector_serch = retriever.invoke(users_input)
        top_indices = extract_video_clip_ids(vector_serch)

        query_for_result = f"""
        SELECT
            vc.video_clip_id AS "videoClipId",
            vc.thumbnail_url AS "thumbnailName",
            vc.summary,
            vc.keyword_character_action AS "keywordCharacterAction",
            vc.start_time AS "startTime",
            vc.end_time AS "endTime", 
            v.video_url AS "videoName", 
            v.play_time AS "playTime", 
            vc.summary || ', ' || vc.keyword_place || ', ' || vc.keyword_mood AS "summary" 
        FROM
            video_clip as vc 
        LEFT JOIN 
            video as v
        ON
            vc.video_id=v.video_id
        """

        cursor.execute(query_for_result)
        response = cursor.fetchall()

        summary_list = []
        for item in response:
            summary_list.append(item[8])

        if len(top_indices) == 0:
            result = []
        else:
            result = []
            for index in top_indices:
                result.append(
                    {
                        "videoClipId": response[index][0],
                        "thumbnailName": response[index][1],
                        "summary": response[index][2],
                        "keywordCharacterAction": response[index][3],
                        "startTime": response[index][4],
                        "endTime": response[index][5],
                        "videoName": response[index][6],
                        "playTime": response[index][7],
                        "videoType": "CJENM",
                    }
                )

            video_presigned_url, thumbnail_presigned_url = generate_url(result=result)

            if video_presigned_url is None:
                raise Exception(f"not found video_presigned_url: {video_presigned_url}")
            else:
                for i in range(len(result)):
                    result[i]["videoUrl"] = video_presigned_url[i]
                    result[i]["thumbnailUrl"] = thumbnail_presigned_url[i]
        return result

    except Exception as e:
        logging.error(f"예상치 못한 오류가 발생했습니다: {e}")


version_api = api.namespace("version", description="version API")


@version_api.route("/")
class Version(Resource):
    def get(self):
        return {"status": "success", "version": app_version}, 200


search_api = api.namespace("search", description="video search")

search_model = search_api.model(
    "Search",
    {"searchQuery": fields.String(required=True, description="검색어를 입력하시오.")},
)


@search_api.route("/")
class Search(Resource):
    @search_api.expect(search_model, validate=True)
    @api.doc(responses={200: "OK", 400: "Bad Request", 500: "Internal Server Error"})
    def post(self):
        if not request.is_json:
            logging.info("Received non-JSON request")
            return {"message": "Bad Request"}, 400

        data = request.get_json()
        search_query = data["searchQuery"]
        conn = None
        try:
            conn = create_connection()
            if conn is None:
                logging.error("Database connection failed")
                return {"message": "DB not connections"}, 500

            logging.info(f"Received search query: {search_query}")

            logging.info("Database connection established")
            cursor = conn.cursor()
            # 코사인 유사도 계산에 필요한 문장을 만들기 위한 쿼리
            query_for_summary = "SELECT summary, keyword_character_action, keyword_place, keyword_mood from video_clip"
            cursor.execute(query_for_summary)
            summary_datas = [
                f"{summary_data[0]} {summary_data[1]}"
                for summary_data in cursor.fetchall()
            ]
            result = search_clips(
                search_text=search_query, summary_datas=summary_datas, cursor=cursor
            )
            print("result", result)

            return {"data": result}, 200

        except Exception as e:
            logging.error(f"{e}")
            return {"message": e}, 500
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# import psycopg2
# import pandas as pd
# import os
# from dotenv import load_dotenv

# # 환경 변수 로드
# load_dotenv()

# # 환경 변수에서 필요한 정보 가져오기
# host = os.environ.get("HOST")
# port = os.environ.get("PORT")
# username = os.environ.get("USERNAME")
# password = os.environ.get("PASSWORD")
# db = os.environ.get("DATABASE")

# def create_connection():
#     """PostgreSQL 데이터베이스에 연결하는 함수"""
#     try:
#         connection = psycopg2.connect(
#             host=host,
#             database=db,
#             user=username,
#             password=password,
#             port=port
#         )
#         return connection
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         return None

# def fetch_data_to_excel():
#     conn = create_connection()
#     if conn is None:
#         return

#     # 전체 테이블 조회하는 쿼리
#     query_for_result = """
#         SELECT *
#         FROM video_clip
#     """

#     try:
#         # 쿼리 실행 후 결과를 데이터프레임으로 변환
#         df = pd.read_sql_query(query_for_result, conn)

#         # 결과를 엑셀 파일로 저장
#         df.to_excel("video_clip_data.xlsx", index=False)
#         print("Data has been written to video_clip_data.xlsx")
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#     finally:
#         conn.close()

# # 함수 실행
# fetch_data_to_excel()
