from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

emb_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en") # Embedding Model
model = OllamaLLM(model="llama3.2:latest", num_ctx=1024) # Main LLM Model
parser = StrOutputParser()

app = FastAPI()

class RAGrequest(BaseModel):
    text : str
    query : str

@app.post("/chat")
def get_answer(payload: RAGrequest):

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(payload.text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    vectorstore = FAISS.from_documents(documents=docs, embedding=emb_model)

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(payload.query)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    template = PromptTemplate(
        template="""
            You are an assistant. Answer the user's question based only on the below document.
            Document: {docs}
            User's question: {query}
            """,
        input_variables=["docs", "query"]
    )
    final_prompt = template.format(docs=context, query=payload.query)

    response = model.invoke(final_prompt)

    return JSONResponse(content={"answer": response})