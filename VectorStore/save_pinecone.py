from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_pinecone import PineconeVectorStore

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

loader = CSVLoader("/Users/bongkyun/10k1m/CjenmVectorStore/keyword_summary.csv")

docs = loader.load()

index_name = "keyword-test"  # "cjenm-data-test"

docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
