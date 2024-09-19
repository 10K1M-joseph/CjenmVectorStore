import os
import sys

from function_descriptions.weather_function_description import weather_function
from function_descriptions.search_functions_description import Users_Search_Function

from apis.weather import proc_weather
from vector_store_pinecone.keyword_vector_pinecone import keyword_extract_video_clip_ids
from vector_store_pinecone.summary_vector_pinecone import summary_extract_video_clip_ids




sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# 모든 함수 목록
all_functions = Users_Search_Function + weather_function


# 사용 가능한 함수 목록을 업데이트하기 위한 함수
# 이 함수는 함수 이름들을 그들의 해당 실행 가능한 api들과 매핑
def update_available_functions():
    functions = all_functions
    available_functions = {}
    for function in functions:
        function_name = function["function"]["name"]

        if function_name.startswith("weather_"):
            available_functions[function_name] = proc_weather

        elif function_name == "keyword_search":
            available_functions[function_name] = keyword_extract_video_clip_ids

        elif function_name == "summary_search":
            available_functions[function_name] = summary_extract_video_clip_ids

    return available_functions
