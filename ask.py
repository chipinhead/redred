import sys
from storage.vector import ask as vector_ask
from typing import List, Dict

def ask(query: str, conversation_history: List[Dict[str, str]] = None) -> str:
    answer = vector_ask(query, conversation_history)
    return answer

def run_repl():
    conversation_history = []
    print("Welcome to the AI assistant. Type 'QUIT' to exit.")
    
    while True:
        query = input("You: ").strip()
        
        if query == "QUIT":
            print("Goodbye!")
            break
        
        if query == "CLEAR":
            conversation_history = []
            print("Conversation history cleared.")
            continue
        
        conversation_history.append({"role": "user", "content": query})
        answer = ask(query, conversation_history)
        print(f"AI: {answer}")
        
        conversation_history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If command-line arguments are provided, use the old behavior
        query = " ".join(sys.argv[1:])
        answer = ask(query)
        print(answer)
    else:
        # If no arguments are provided, start the REPL
        run_repl()
