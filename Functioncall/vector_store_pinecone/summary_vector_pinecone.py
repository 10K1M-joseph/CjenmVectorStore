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


def summary_extract_video_clip_ids(text):
    video_clip_ids = []
    results = retriever.invoke(text)

    print("1번", results[0].page_content)
    print("2번", results[1].page_content)
    print("3번", results[2].page_content)
    print("4번", results[3].page_content)
    print("5번", results[4].page_content)

    for doc in results:
        page_content = doc.page_content.lstrip("\ufeff")  # BOM 문자 제거
        for line in page_content.splitlines():
            if line.startswith("videoClipId:"):
                video_clip_id = line.split(":")[1].strip()  # ':' 뒤의 숫자 추출
                video_clip_ids.append(int(video_clip_id))
    return video_clip_ids


# print(summary_extract_video_clip_ids("형사가 범인을 잡는 장면"))