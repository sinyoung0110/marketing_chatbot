from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()
embedding=OpenAIEmbeddings(
    model='text-embedding-3-small',
    api_key=os.getenv("OPENAI_API_KEY")
)

from langchain_openai import ChatOpenAI

#언어 모델 불러오기
from langchain_core.caches import BaseCache
from langchain_core.callbacks import Callbacks
ChatOpenAI.model_rebuild()
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(model="gpt-4o-mini")

from langchain_chroma import Chroma
print("Loading existing Chroma store")
persist_directory='/Users/sinyoung/myllmclass/week9/chroma_store'

vectorsotre=Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)

#create retriever
retriever=vectorsotre.as_retriever(k=3)

#create document chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

question_answering_prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "사용자의 질문에 대해 아래 context에 기반하여 답변하라. \n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

def combine_context(context):
    if isinstance(context,list):
        return "\n\n".join(str(c.page_content) if hasattr(c, "page_content") else str(c) for c in context)
    return str(context)

document_chain=(
    RunnablePassthrough.assign(context=lambda x: combine_context(x["context"]))
    |  question_answering_prompt
    |  llm
    |  StrOutputParser()
)

#query augmentation chain
query_augmentation_prompt=ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="messages"),
    (
        "system",
        "기존의 대화 내용을 활영하여 사용자가 질문한 의도를 파악해서 한 문장의 명료한 질문으로 변환하라. 대명사나 이, 저, 그와 같은 표현을 명확한 명사로 변환하라. :\n\n{query}"
    ),
])

query_augmentation_prompt=query_augmentation_prompt | llm | StrOutputParser()