"""
rag.py — builds the conversational RAG chain
ChromaDB + HuggingFace local embeddings + Gemma 4
"""

import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def build_rag_chain(blood_report_text: str):

    # Split report into small searchable chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents([blood_report_text])

    # Local embeddings — no API key, runs on your machine
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Store chunks as vectors in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="blood_report"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(
        model="gemma-4-31b-it",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )

    # Prompt — allows BOTH report-specific AND general medical questions
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a knowledgeable, friendly health assistant — like a doctor having a real conversation with a patient.

You have the patient's blood report and analysis for reference:
{context}

Guidelines:
- Answer ANY health or medical question using your medical knowledge — not only what is in the report.
- If the question is about their specific results (e.g. "is my hemoglobin ok?"), refer to their actual values from the context.
- If the question is general (e.g. "what causes diabetes?", "what is anemia?", "is fasting good?"), answer freely using medical knowledge even if not in the report.
- Be warm, clear, and conversational — like a doctor explaining to a patient, not reading data off a screen.
- Only remind them to see a real doctor when it is genuinely important (not every message).
"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x["input"]))
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    store = {}

    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )