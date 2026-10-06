# GenAI Agent Backend

A Generative AI backend built with **LangGraph, Google Gemini, FastAPI, PostgreSQL, RAG, and tool calling**.

The project demonstrates how to build an LLM-powered backend that can authenticate users, maintain conversation state, retrieve information from local documents, search the web, and expose the AI system through REST APIs.

## 🚀 Features

* **LLM Agent** powered by Google Gemini
* **LangGraph** for agent orchestration and workflow management
* **Tool Calling** with:

  * Web Search using Tavily
  * Local document retrieval using ChromaDB
* **RAG** using vector embeddings and semantic search
* **Conversation Checkpointing** using PostgreSQL
* **JWT Authentication**
* **Argon2 Password Hashing**
* **FastAPI** REST API
* **PostgreSQL** for user authentication data and LangGraph checkpoint persistence
* **Environment-based configuration** using `.env`

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

### Authentication Flow

```text
Client
  ↓
/register
  ↓
FastAPI
  ↓
Argon2 Password Hash
  ↓
PostgreSQL Users Table
```

```text
Client
  ↓
/login
  ↓
PostgreSQL Users Table
  ↓
Verify Password
  ↓
JWT Access Token
  ↓
Authenticated Requests
```

## 🔄 Agent Workflow

The agent follows a tool-calling workflow:

```text
User
  ↓
FastAPI
  ↓
LangGraph
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

The agent can decide between:

* **Web Search** → Tavily
* **Local Retrieval** → ChromaDB

## 🛠️ Tech Stack

| Technology    | Purpose                                        |
| ------------- | ---------------------------------------------- |
| Python        | Core programming language                      |
| FastAPI       | REST API and backend                           |
| LangGraph     | Agent orchestration and state management       |
| LangChain     | LLM and tool integration                       |
| Google Gemini | Large Language Model                           |
| ChromaDB      | Vector database and local RAG                  |
| Tavily        | Web search                                     |
| PostgreSQL    | User data and LangGraph checkpoint persistence |
| JWT           | Authentication                                 |
| Argon2        | Secure password hashing                        |
| Pydantic      | Request data validation                        |

## 📂 Project Structure

```text
llm-agent-backend/
│
├── main.py       # FastAPI application, LangGraph agent, and API endpoints
├── auth.py       # User registration and login
├── schema.py     # Pydantic request schemas
├── sec.py        # Password hashing and JWT authentication
├── tools.py      # Web search and local RAG tools
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔑 API Endpoints

### Register

```http
POST /register
```

Creates a new user account and stores the user information in the PostgreSQL `Users` table.

Example request:

```json
{
  "FirstName": "Yousef",
  "LastName": "Salah",
  "age": 25,
  "email": "user@example.com",
  "password": "your_password"
}
```

### Login

```http
POST /login
```

Authenticates the user and returns a JWT access token.

Example request:

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

Example response:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

### Chat

```http
POST /chat
```

Requires a valid authentication token and sends a user message to the LangGraph agent.

Example request:

```json
{
  "user_input": "Search the web for the latest information about LangGraph."
}
```

The agent can decide whether to answer directly or use one of its available tools.

## 🗄️ Database Setup

The project requires an **existing PostgreSQL database**.

The application uses PostgreSQL for:

1. **User authentication data**
2. **LangGraph checkpoint persistence**

The project does **not** create the PostgreSQL database itself.

### Users Table

The authentication system expects a `Users` table with the following structure:

```sql
CREATE TABLE Users (
    user_ID SERIAL PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

After creating the database, configure the connection in `.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

> **Note:** The current authentication implementation in `auth.py` uses its own PostgreSQL connection settings, while `DATABASE_URL` is used by LangGraph's `PostgresSaver`. These can be unified in a future refactor.

## 💾 LangGraph Checkpointing

The project uses `PostgresSaver` to persist LangGraph checkpoints.

This allows the agent to maintain state across requests instead of keeping the conversation state only in application memory.

During startup, LangGraph initializes the required checkpoint tables inside the configured PostgreSQL database.

```python
checkpointer.setup()
```

This does **not** create the PostgreSQL database itself. The PostgreSQL database must already exist.

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_application_secret
SECRET_KEY_MODEL=your_google_gemini_api_key
SECRET_KEY_SEARCH=your_tavily_api_key

DATABASE_URL=postgresql://username:password@localhost:5432/database_name

ALGORITHM=HS256
```

### Environment Variables

| Variable            | Purpose                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| `SECRET_KEY`        | JWT signing secret and database password in the current implementation |
| `SECRET_KEY_MODEL`  | Google Gemini API key                                                  |
| `SECRET_KEY_SEARCH` | Tavily API key                                                         |
| `DATABASE_URL`      | PostgreSQL connection string for LangGraph checkpointing               |
| `ALGORITHM`         | JWT signing algorithm                                                  |

> **Security:** Never commit `.env` or API keys to GitHub.

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/Yousef-salah-Ma/llm-agent-backend.git

cd llm-agent-backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in `.env`.

Make sure PostgreSQL is running and the required database and `Users` table already exist.

Run the FastAPI application:

```bash
uvicorn main:app --reload
```

The interactive API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

## 🧪 Example Usage

After starting the server:

### 1. Register

```text
POST /register
```

### 2. Login

```text
POST /login
```

Copy the returned JWT access token.

### 3. Authenticate

Use the token when calling:

```text
POST /chat
```

### 4. Send a message

```json
{
  "user_input": "What is the latest version of LangGraph?"
}
```

The LangGraph agent can determine whether it needs to use the web search tool or local RAG.

## 🎯 What I Learned

This project helped me understand how different Generative AI components work together in a complete backend system:

* Building LLM-powered applications beyond simple prompting
* LLM tool calling
* Agent orchestration with LangGraph
* Conditional agent workflows
* RAG and vector retrieval
* Web search integration
* Conversation state and checkpoint persistence
* JWT authentication
* Secure password hashing with Argon2
* Integrating LLM applications with FastAPI
* Connecting AI agents with PostgreSQL
* Building an authenticated AI backend

## 🔮 Future Improvements

Planned improvements include:

* Advanced RAG and reranking
* LLM evaluation
* Observability and tracing
* Streaming AI responses
* Improved conversation/thread management
* Automated testing
* Docker deployment
* Production deployment
* Improved configuration and secret management
* Better multilingual retrieval for Arabic and English documents

## 👨‍💻 Author

**Yousef Salah**

AI & Machine Learning Engineer focused on **Generative AI, LLMs, RAG, and AI Agents**.

GitHub:
https://github.com/Yousef-salah-Ma

---
