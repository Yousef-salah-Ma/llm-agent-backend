# GenAI Agent Backend

A production-oriented Generative AI backend built with **LangGraph, Gemini, FastAPI, PostgreSQL, RAG, and tool calling**.

The project demonstrates how to build an LLM-powered backend that can maintain conversation state, retrieve information from local documents, search the web, and expose the AI system through authenticated APIs.

## 🚀 Features

* **LLM Agent** using Google Gemini
* **LangGraph** for agent orchestration and workflow management
* **Tool Calling** with:

  * Web Search using Tavily
  * Local document retrieval using ChromaDB
* **RAG** using vector embeddings and semantic search
* **Conversation Checkpointing** using PostgreSQL
* **JWT Authentication**
* **Argon2 Password Hashing**
* **FastAPI** REST API
* **PostgreSQL** for user data and persistent agent state
* Environment-based configuration using `.env`

## 🧠 Architecture

```text
                    Client
                       │
                       ▼
                  FastAPI API
                       │
                       ▼
               JWT Authentication
                       │
                       ▼
                  LangGraph
                       │
                       ▼
                    Gemini
                   /      \
                  /        \
                 ▼          ▼
          Web Search      Local RAG
             Tavily        ChromaDB
                 \          /
                  \        /
                   ▼      ▼
                    Gemini
                       │
                       ▼
             PostgreSQL Checkpoint
                       │
                       ▼
                    Response
```

## 🔄 Agent Workflow

The agent follows a tool-calling workflow:

```text
User
  ↓
LLM
  ↓
Does the LLM need a tool?
  ├── No → Final Answer
  │
  └── Yes
       ↓
    Tool Call
       ↓
    Tool Execution
       ↓
    Tool Result
       ↓
      LLM
       ↓
   Final Answer
```

## 🛠️ Tech Stack

| Technology    | Purpose                    |
| ------------- | -------------------------- |
| Python        | Core programming language  |
| FastAPI       | Backend API                |
| LangGraph     | Agent orchestration        |
| LangChain     | LLM and tool integration   |
| Google Gemini | Large Language Model       |
| ChromaDB      | Vector database / RAG      |
| Tavily        | Web search                 |
| PostgreSQL    | Database and checkpointing |
| JWT           | Authentication             |
| Argon2        | Password hashing           |
| Pydantic      | Data validation            |

## 📂 Project Structure

```text
llm-agent-backend/
│
├── main.py       # FastAPI application and API endpoints
├── auth.py       # User registration and login
├── schema.py     # Pydantic request schemas
├── sec.py        # Password hashing and JWT authentication
├── tools.py      # Web search and local RAG tools
└── README.md
```

## 🔑 API Endpoints

### Register

```http
POST /register
```

Creates a new user account.

### Login

```http
POST /login
```

Authenticates the user and returns a JWT access token.

### Chat

```http
POST /chat
```

Requires authentication and sends a user message to the LangGraph agent.

Example request:

```json
{
  "user_input": "Search the web for the latest information about LangGraph."
}
```

## ⚙️ Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_database_or_application_secret
SECRET_KEY_MODEL=your_google_gemini_api_key
SECRET_KEY_SEARCH=your_tavily_api_key
DATABASE_URL=your_postgresql_connection_string
ALGORITHM=HS256
```

**Never commit your `.env` file or API keys to GitHub.**

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/Yousef-salah-Ma/llm-agent-backend.git

cd llm-agent-backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in `.env`.

Run the FastAPI application:

```bash
uvicorn main:app --reload
```

The API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

## 🎯 What I Learned

This project helped me understand how different GenAI components work together in a complete application:

* LLM tool calling
* Agent orchestration with LangGraph
* RAG and vector retrieval
* Web search integration
* Conversation persistence
* Authentication for AI APIs
* Connecting LLM applications with backend services

## 🔮 Future Improvements

Planned improvements include:

* Advanced RAG and reranking
* LLM evaluation
* Observability and tracing
* Streaming AI responses
* Docker deployment
* Improved conversation/thread management
* Automated testing
* Production deployment

## 👨‍💻 Author

**Yousef Salah**

AI & Machine Learning Engineer focused on Generative AI, LLMs, RAG, and AI Agents.
