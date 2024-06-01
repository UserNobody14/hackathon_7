from utils.llm import llm
from utils.retrieve import retriever
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

template = """You are an assistant for a video creator. You are given a request and a context. You need to write a short concise script based on the context and the request.
Question: {question} 
Context: {context} 
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


def gen_script_from_text(text: str):
    """
    Generate a script from text
    :param text: text
    :return: script
    """
    # Search for the most similar script/video
    return chain.invoke(text)
