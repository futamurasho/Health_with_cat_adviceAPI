from pathlib import Path
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def initialize_vector_store() -> Chroma:
    embeddings = OpenAIEmbeddings()

    vector_store_path = "vec/note.db"
    if Path(vector_store_path).exists():
        vector_store = Chroma(embedding_function=embeddings, persist_directory=vector_store_path)
    else:
        # CSVファイルのロード
        loader = CSVLoader(file_path="../my_resource/nutrition_data.csv")
        docs = loader.load()

        # テキスト分割
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        vector_store = Chroma.from_documents(
            documents=splits, embedding=embeddings, persist_directory=vector_store_path
        )
    return vector_store

def initialize_retriever() -> VectorStoreRetriever:
    vector_store = initialize_vector_store()
    return vector_store.as_retriever()

def initialize_chain() -> RunnableSequence:
    llm = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0)
    retriever = initialize_retriever()
    template = (
        "今からあることをやってもらう、要求内容は以下の通りである。"
        "{question}"
        "そして、栄養素に関しては次のcontextをもとに回答してください\n"
        "{context}\n"
    )
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt
        | llm
    )
    return chain
