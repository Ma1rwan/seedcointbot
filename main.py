from bot.create_session import create_session
from bot.lancher import launcher
from colorama import Fore, Style, init
import time
# Initialize colorama for Windows compatibility
init(autoreset=True)

def display_logo():
    # Display the program's logo with "SEEDBOT"
    print(f"{Fore.CYAN}{Style.BRIGHT} _____ _____ _________________  _____ _____ ")
    print(f"{Fore.CYAN}{Style.BRIGHT}/  ___|  ___|  ___|  _  \ ___ \|  _  |_   _|")
    print(f"{Fore.CYAN}{Style.BRIGHT}\ `--.| |__ | |__ | | | | |_/ /| | | | | |  ")
    print(f"{Fore.CYAN}{Style.BRIGHT} `--. \  __||  __|| | | | ___ \| | | | | |  ")
    print(f"{Fore.CYAN}{Style.BRIGHT}/\__/ / |___| |___| |/ /| |_/ /\ \_/ / | |  ")
    print(f"{Fore.CYAN}{Style.BRIGHT}\____/\____/\____/|___/ \____/  \___/  \_/   ")
    print('\n')
    # Display the GitHub link
    print(f"{Fore.YELLOW}GitHub: {Fore.GREEN}https://github.com/Ma1rwan")
    print(f"{Fore.YELLOW}Join us on Telegram: {Fore.BLUE}https://t.me/+3ozlUUBMlSo2OGY0")
    # Add a pause for effect
    time.sleep(2)

def run_selected_module():
    display_logo()
    while True:
        # Display options to the user
        print('\n')
        print(
        f"{Fore.YELLOW}Note: {Fore.GREEN}To ensure the bot works efficiently, you need to include at least 3 accounts.")
        print(f"{Fore.YELLOW}The more accounts you add, the more profit the bot will generate overall!")

        print("\nChoose an option:")
        print("1. Create Session.")
        print("2. Launch bot.")
        print("3. Exit.")

        choice = input("Enter 1, 2, or 3: ")

        # Run the chosen option
        if choice == '1':
            try:
                create_session()  # This runs the session creation code directly
            except Exception as e:
                print(f"Error: {str(e)}")
        elif choice == '2':
            try:
                launcher()  # Calls the bot launching function
            except ImportError:
                print("Error: bot.lancher module not found.")
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Example usage
if __name__ == "__main__":
    run_selected_module()