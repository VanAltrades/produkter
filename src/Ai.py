# https://github.com/NidheeshaT/vertexai-api/blob/master/main.py
from flask import Flask,request,make_response, jsonify
from vertexai.preview.language_models import ChatModel,ChatSession,ChatMessage
import dotenv
import json,os
dotenv.load_dotenv()

if os.environ.get("PROJECT_ID"):
    PARENT = f"projects/{os.environ.get('PROJECT_ID')}"
if not os.path.exists("./secret.json"):
    if os.environ.get("CREDENTIALS"):
        with open("secret.json","w") as f:
            f.write(os.environ.get("CREDENTIALS"))

support_context="You are a product content writer with a specialty in SEO. You are tasked with describing products and explaining how they are used, what industries they are used in, who uses them, and frequently asked questions."
bison_model=ChatModel.from_pretrained("chat-bison@001")

def palm(message:str,context:str,history:list):
    valid_history=[]
    for i,h in enumerate(history):
        if "content" in h and "author" in h:
            valid_history.append(ChatMessage(h["content"],h['author']))
    chat=ChatSession(model=bison_model,context=context,message_history=valid_history,temperature=0.94)
    response=chat.send_message(message)
    return response

def query():
    try:
        req_data=request.json #message,context,history:list of chat messages
        message=req_data.get("message")
        context=req_data.get("context","")
        history=req_data.get("history",[])
        response=palm(message,context,history)
        return f"{response}"
    except Exception as e:
        return make_response("Server error",500)

def support():
    try:
        req_data=request.json #message,context,history:list of chat messages
        message=req_data.get("message")
        context=req_data.get("context","")
        history=req_data.get("history",[])
        response=palm(message,support_context+context,history)
        return f"{response}"
    except Exception as e:
        return make_response("Server error",500)
