from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document

# from langchain_community.embeddings import OctoAIEmbeddings
import uuid
from langchain_community.vectorstores import FAISS


load_dotenv()
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_TOKEN"]


# embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)


def turn_video_and_script_files_into_vectordb(directory):
    """
    Scan through a directory and send all video and script files to the vector store
    :param directory: directory to scan. This dir should have video (.mp4) and script (.txt) files
    :return: None
    """
    docs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                video_file = os.path.join(root, file)
                script_file = video_file.replace(".mp4", ".txt")
                possible_script_files = [
                    video_file.replace(".mp4", ".txt"),
                    video_file.replace(file, "context.txt"),
                ]
                for possible_script_file in possible_script_files:
                    if os.path.exists(possible_script_file):
                        script_file = possible_script_file
                        break
                if os.path.exists(script_file):
                    print(f"Processing {video_file} and {script_file}")
                    with open(script_file, "r") as f:
                        script = f.read()
                        # Send to vector store
                        document = video_and_script_to_vectordb(
                            video_file, script_file, script
                        )
                        docs += document
                else:
                    print(f"Script file not found for {video_file}")
            else:
                print(f"Skipping {file}")
    if len(docs) > 0:
        print(f"Processed {len(docs)} documents")

        return FAISS.from_documents(documents=docs, embedding=embeddings)
    else:
        print("Error: No documents processed!!!!!!")


def video_and_script_to_vectordb(video_file, script_file, script):
    """
    Send a video and script to the vector store
    :param video_file: path to the video file
    :param script_file: path to the script file
    :param script: script content
    :return: Document
    """
    # Split the script into chunks
    chunk_size = 1024
    chunk_overlap = 128
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_text(script)
    docs = []
    for split in splits:
        doc = Document(
            id=str(uuid.uuid4()),
            page_content=split,
            metadata={"video_file": video_file, "script_file": script_file},
        )
        docs.append(doc)
    return docs
