import os
from src.core.config import config
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from src.core.db import weaviate_client

os.environ["HUGGINGFACEHUB_API_TOKEN"] = config.HUGGINGFACEHUB_API_TOKEN


embeddings = HuggingFaceHubEmbeddings()


db = WeaviateVectorStore(
    index_name="paper",
    text_key="content",
    embedding=embeddings,
    client=weaviate_client
    )
