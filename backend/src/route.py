#route.py
from src.util.DocChainUtil import getDocChainAnswer
from src.database.SQLDatabase import db
from src.util.SQLDatabaseChainUtil import getSQLChainAnswer


def pick_tool(query, chat_history):

    chat_history.chat_memory.add_user_message(query)

    if 'SQL' in query:
        response = getSQLChainAnswer(query, db, chat_history)
    else: 
        response = getDocChainAnswer(query, chat_history)
    
    chat_history.chat_memory.add_ai_message(response)

    return response