import sys
import os
from dotenv import load_dotenv
from ai_engine import LearnBuddyEngine

def print_banner():
    banner = r"""
================================================================================
    __                            ____             __     __      
   / /   ___  ____ __________  __/ __ )__  _______  / /____/ /_  __
  / /   / _ \/ __ `/ ___/ __ \/ / __  / / / / ___/ / / __  / / / / /
 / /___/  __/ /_/ / /  / / / / / /_/ / /_/ / /__  / / /_/ / /_/ /_/ 
/_____/\___/\__,_/_/  /_/ /_/_/_____/\__,_/\___/ /_/\__,_/\__, ( )  
                                                         /____/|/   
================================================================================
                     Your Elite Bite-Sized AI Learning Coach
================================================================================
"""
    print(banner)

def get_multiline_input(prompt_text):
    print(prompt_text)
    print(" (Press Enter on an empty line when finished, or type your answer directly)")
    lines = []
    while True:
        try:
            line = input("> ").strip()
            if not line:
                break
            lines.append(line)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            sys.exit(0)
    return " ".join(lines) if lines else ""

def main():
    # Load environment variables from .env
    load_dotenv()
    
    # Check if GEMINI_API_KEY is present
    if not os.getenv("GEMINI_API_KEY"):
        print("[Error] GEMINI_API_KEY not found in environment variables.")
        print("Please check your .env file or environment variables.")
        sys.exit(1)

    print_banner()

    try:
        # Prompting user for setup
        print("Let's configure your personalized learning session:")
        concept = input("1. What concept or topic do you want to learn today?\n> ").strip()
        while not concept:
            concept = input("Please specify a concept:\n> ").strip()

        profile = input("2. What is your current background/skill level in this topic?\n> ").strip()
        while not profile:
            profile = input("Please specify your current background/skill level:\n> ").strip()

        print("\n[LearnBuddy] Spin-up in progress... initializing engine...")
        engine = LearnBuddyEngine()

        print("[LearnBuddy] Generating your personalized lesson plan...\n")
        first_milestone = engine.start_learning_session(concept, profile)
        
        print("================================================================================")
        print(first_milestone)
        print("================================================================================")

        # Chat loop
        while True:
            print("\nType your response to the Pulse-Check (or type 'exit' to quit):")
            try:
                user_msg = input("User > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nGoodbye! Happy learning!")
                break
                
            if not user_msg:
                continue
            if user_msg.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! Happy learning!")
                break
                
            print("\n[LearnBuddy] Thinking...")
            try:
                response_text = engine.send_message(user_msg)
                print("\n================================================================================")
                print(response_text)
                print("================================================================================")
            except Exception as e:
                print(f"\n[Error] Failed to get response: {e}")
                
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
