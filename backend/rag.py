import os
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class RAGProcessor:
    def __init__(self):
        # Validate API key
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise Exception("GROQ_API_KEY not found in environment variables")
        
        print(f"Groq API key loaded: {groq_api_key[:10]}...")
        
        try:
            self.emb_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
            self.groq_model = ChatGroq(
                api_key=groq_api_key,
                model="llama-3.1-8b-instant",
                temperature=0
            )
            print("RAG processor models initialized successfully")
        except Exception as e:
            raise Exception(f"Error initializing models: {e}")
        
        self.supported_languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'tr': 'Turkish', 'pl': 'Polish', 'nl': 'Dutch', 'sv': 'Swedish',
            'da': 'Danish', 'no': 'Norwegian', 'fi': 'Finnish', 'he': 'Hebrew'
        }
    
    def detect_language(self, text: str) -> str:
        lang_patterns = {
            'es': ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no'],
            'fr': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir'],
            'de': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich']
        }
        
        text_lower = text.lower()
        scores = {}
        
        for lang, words in lang_patterns.items():
            score = sum(1 for word in words if word in text_lower)
            scores[lang] = score
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'en'
    
    def process_query(self, text: str, query: str, target_lang: str = 'en') -> dict:
        try:
            detected_lang = self.detect_language(text)
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_text(text)
            docs = [Document(page_content=chunk) for chunk in chunks]
            
            vectorstore = FAISS.from_documents(documents=docs, embedding=self.emb_model)
            retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            relevant_docs = retriever.invoke(query)
            
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            template = PromptTemplate(
                template="""
                You are a multilingual AI assistant. Answer the user's question based on the provided document.
                
                Document: {docs}
                User's question: {query}
                
                IMPORTANT: You MUST respond in {target_lang} language.
                If the target language is not English, translate your entire response to {target_lang}.
                Provide a clear, comprehensive answer in {target_lang}.
                """,
                input_variables=["docs", "query", "target_lang"]
            )
            
            final_prompt = template.format(
                docs=context, 
                query=query, 
                target_lang=self.supported_languages.get(target_lang, 'English')
            )
            
            response = self.groq_model.invoke(final_prompt)
            
            return {
                'answer': response.content,
                'detected_language': detected_lang,
                'target_language': target_lang
            }
            
        except Exception as e:
            return {
                'answer': f"Error processing query: {str(e)}",
                'detected_language': 'en',
                'target_language': target_lang
            }