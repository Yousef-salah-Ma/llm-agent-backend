from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from schema import login_users , Create_Account , messegas
from auth import  Register , login 
from sec import get_current_user
from langgraph.prebuilt import ToolNode
from langgraph.graph import add_messages , START , END , StateGraph 
from langgraph.graph import MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from fastapi import FastAPI, Depends , HTTPException
from langgraph.checkpoint.postgres import PostgresSaver
import os
from tools import (
    web_search,
    local_search,
)
load_dotenv()
SECRET_KEY_MODEL  = os.getenv("SECRET_KEY_MODEL")
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=SECRET_KEY_MODEL
)

llm  = llm.bind_tools([  web_search,local_search])

tool_node = ToolNode([  web_search,local_search])
def llm_node(state):
    response = llm.invoke(state["messages"])



    return {
        "messages": [response]
    }
graph = StateGraph(MessagesState)

graph.add_node("llm" , llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START , "llm")
graph.add_edge("tools", "llm")

def route(state):
    last_message = state["messages"][-1]



    if last_message.tool_calls:
        return "tools"

    return "end"


graph.add_conditional_edges("llm" ,route ,{
    "tools":"tools",
    "end":END
} )



DATABASE_URL= os.getenv("DATABASE_URL")

cm = PostgresSaver.from_conn_string(DATABASE_URL)

checkpointer = cm.__enter__()
checkpointer.setup()

model = graph.compile(
        checkpointer=checkpointer
    )

app = FastAPI()

@app.post("/login")
def login_(login_sch : login_users ):

        passowrd = login_sch.password
        email = login_sch.email 

        return    login(passowrd , email)

@app.post("/register")
def register_(data: Create_Account ):
     email = data.email 
     password = data.password 
     FirstName = data.FirstName
     last_name = data.LastName 
     age = data.age

     return  Register(FirstName , last_name , age ,  email , password )

@app.post("/chat")
def chat(
    message: messegas,
    token: str = Depends(get_current_user)
):
    
    config = {
            "configurable": {
                "thread_id": token
            }
        }
    
    res = model.invoke({"messages":[HumanMessage(message.user_input)]} , config)
    

    return {
        "response":res["messages"][-1].text,
        
    }

       