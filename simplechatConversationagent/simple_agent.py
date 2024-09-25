from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv

# Load environment variables and initialize the language model
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000, temperature=0)

# Create a simple in-memory store for chat histories
store = {}

def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Combine the prompt and model into a runnable chain
chain = prompt | llm

# Wrap the chain with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Example usage
def chat_with_ai(session_id: str, user_input: str):
    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    return response.content

# Main interaction loop
if __name__ == "__main__":
    session_id = "user_123"
    print("AI Assistant: Hello! How can I help you today? (Type 'exit' to end the conversation)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("AI Assistant: Goodbye! Have a great day!")
            break
        
        ai_response = chat_with_ai(session_id, user_input)
        print(f"AI Assistant: {ai_response}")
    
    # Print conversation history
    print("\nConversation History:")
    for message in store[session_id].messages:
        print(f"{message.type}: {message.content}")