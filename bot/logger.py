from datetime import datetime
from colorama import init, Fore
# Initialize colorama
init(autoreset=True)


class Logger:
    def __init__(self, tag="SEEDBOT"):
        self.tag = tag

    def _log(self,session_name, level, message, level_color, tag_color, message_color):
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        orange = "\033[38;5;214m"  # ANSI escape code for orange
        # Format and print the log message with colors
        if "uncommon" in message:
            message = message.replace("uncommon", f"{Fore.GREEN}uncommon{message_color}")
        elif "common" in message:
            message = message.replace("common", f"{Fore.LIGHTGREEN_EX}common{message_color}")

        if "rare" in message:
            message = message.replace("rare", f"{Fore.BLUE}rare{message_color}")
        if "epic" in message:
            message = message.replace("epic", f"{Fore.MAGENTA}epic{message_color}")
        if "legendary" in message:
            message = message.replace("legendary", f"{orange}legendary{message_color}")
        print(
            f"{Fore.LIGHTWHITE_EX}[{timestamp}] | {level_color}{level:<8}{Fore.LIGHTWHITE_EX} | {tag_color}{self.tag} {message_color}| {session_name} | {message}")

    def info(self, session_name, message):
        """Log an informational message"""
        self._log(session_name, "INFO", message, Fore.BLUE, Fore.GREEN, Fore.LIGHTWHITE_EX)

    def success(self, session_name, message):
        """Log a success message"""
        self._log(session_name, "SUCCESS", message, Fore.GREEN, Fore.GREEN, Fore.LIGHTWHITE_EX)

    def error(self, session_name, message):
        """Log an error message"""
        self._log(session_name, "ERROR", message, Fore.RED, Fore.GREEN, Fore.LIGHTWHITE_EX)

    def unknown(self, session_name, message):
        """Log a message with unknown level"""
        self._log(session_name, "UNKNOWN", message, Fore.LIGHTWHITE_EX, Fore.GREEN, Fore.LIGHTWHITE_EX)
