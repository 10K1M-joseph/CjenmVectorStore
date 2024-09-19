from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


# 환경 변수 로드
load_dotenv()


index_name = "cjenm-data-test"
# index_name = "keyword-test"
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
# results = retriever.invoke("행복한 날")


def extract_video_clip_ids(results):
    video_clip_ids = []
    for doc in results:
        page_content = doc.page_content.lstrip("\ufeff")  # BOM 문자 제거
        for line in page_content.splitlines():
            if line.startswith("videoClipId:"):
                video_clip_id = line.split(":")[1].strip()  # ':' 뒤의 숫자 추출
                video_clip_ids.append(int(video_clip_id))
    return video_clip_ids



# def pretty_print_documents(docs):
#     for doc in docs:
#         print(f"{'-'*80}")
#         print(f"Row: {doc.metadata['row']}")
#         print(f"Source: {doc.metadata['source']}")
#         print("Content:")
#         # BOM 제거 및 page_content 줄 단위 출력
#         for line in doc.page_content.lstrip('\ufeff').splitlines():
#             print(f"  {line}")
#         print(f"{'-'*80}\n")

# pretty_print_documents(retriever.invoke("경찰서"))
# videoClipId 추출 실행
# video_clip_ids = extract_video_clip_ids(results)
# print(video_clip_ids)


# def clip_id_match(clip_ids, video_clip_ids):
#     matched_clip_ids = []
#     for clip_id in clip_ids:
#         if str(clip_id) in video_clip_ids:
#             matched_clip_ids.append(clip_id)
#     return matched_clip_ids


# print("-"* 10)
# print("video clip 번호: ", clip_id_match(clip_ids, video_clip_ids))
