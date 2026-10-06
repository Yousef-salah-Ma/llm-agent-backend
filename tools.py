from tavily import TavilyClient
from langchain_core.tools import tool
import chromadb 
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os 
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY_SEARCH  = os.getenv("SECRET_KEY_SEARCH")
client = TavilyClient( SECRET_KEY_SEARCH)


@tool
def web_search(question: str):
        """
        Search the internet for information that requires up-to-date,
        current, or external web-based knowledge.

        Use this tool when:
        - The user asks about recent or current information.
        - The user asks about news, current events, prices, or live information.
        - The answer may have changed since the model's knowledge cutoff.
        - The user explicitly asks you to search the web.
        - The required information is not available in the local documents.

        Do not use this tool for general questions that can be answered
        reliably without external information.

        Input:
        question: The user's question or search query.
        """
        
        if not question.strip():
            return "Search query is empty."

        if question.strip().startswith("site:"):
            return "Please provide actual search terms, not only a site: operator."

        response = client.search(
            query=question,
            include_answer="basic",
            search_depth="basic",
            max_results=1
        )


        ret = ""

        for i in response["results"]:
            ret += i["content"] + "\nمرجع: " + i["url"] + "\n"

        return ret





embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
client2 = chromadb.PersistentClient(path="./nvidia")

collection  = client2.get_or_create_collection(name="collection" ,embedding_function=embedding_function  )
@tool

def local_search(question: str):
        """
        Search the local NVIDIA documents for relevant information.

        Use this tool when the user's question can be answered
        using information from the local NVIDIA document collection.

        Do not use this tool for general knowledge, calculations,
        or information that requires an internet search.

        Input:
            question: A natural-language question about the NVIDIA documents.

        Returns:
            The most relevant passages retrieved from the local documents.
        """

        result = collection.query(
            query_texts=[question],
            n_results=5
        )

        documents = result["documents"][0]

        if not documents:
            return "No relevant information was found in the local documents."

        return "\n\n".join(documents)



