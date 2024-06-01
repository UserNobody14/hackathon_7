from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OctoAIEmbeddings

embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")


vector_store = Milvus(
    #     splits,
    embeddings,
    connection_args={"host": "localhost", "port": 19530},
    collection_name="webscraped3",
)
