import re
from lab_1 import get_logs_list
from tools import LOG_MESSAGE, parse_ssh_log

IPV4_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
USER_NAME_PATTERN = r"user\s+(?P<user>\w+)"
ACCEPTED_USER_PATTERN = r"Accepted password for (\w+)"
FIRST_MATCH = 1
ACCEPTED_LOGGING_MESSAGE_PATTERN = r"Accepted"
FAILED_PASSWORD_MESSAGE_PATTERN = r"Invalid password for"
INVALID_USER_MESSAGE_PATTERN = r"Invalid user (\w+)"
DISCONNECTED_MESSAGE_PATTERN = r"Received disconnect"
FAILED_LOGGING_MESSAGE_PATTERN = r"Failed password for"
POSSIBLE_BREAK_IN_MESSAGE_PATTERN = r"POSSIBLE BREAK-IN ATTEMPT!"
ACCEPTED_LOGGING_MESSAGE = "udane logowanie"
FAILED_PASSWORD_MESSAGE = "błędne hasło"
INVALID_USER_MESSAGE = "błędna nazwa użytkownika"
DISCONNECTED_MESSAGE = "zamknięcie połączenia"
FAILED_LOGGING_MESSAGE = "nieudane logowanie"
POSSIBLE_BREAK_IN_MESSAGE = "próba włamania"
OTHER_MESSAGE = "inne"


MESSAGE_PATTERN_DICT = {
    ACCEPTED_LOGGING_MESSAGE_PATTERN: ACCEPTED_LOGGING_MESSAGE,
    FAILED_PASSWORD_MESSAGE_PATTERN: FAILED_PASSWORD_MESSAGE,
    DISCONNECTED_MESSAGE_PATTERN: DISCONNECTED_MESSAGE,
    INVALID_USER_MESSAGE_PATTERN: INVALID_USER_MESSAGE,
    POSSIBLE_BREAK_IN_MESSAGE_PATTERN: POSSIBLE_BREAK_IN_MESSAGE,
    FAILED_LOGGING_MESSAGE_PATTERN: FAILED_LOGGING_MESSAGE,
}


def get_ipv4s_from_log(ssh_log_dict):
    ipv4_regex = re.compile(IPV4_PATTERN)
    ipv4s = ipv4_regex.findall(ssh_log_dict[LOG_MESSAGE])
    return ipv4s


def get_user_from_log(ssh_log_dict):
    match = re.search(USER_NAME_PATTERN, ssh_log_dict[LOG_MESSAGE])
    if not match:
        match = re.search(ACCEPTED_USER_PATTERN, ssh_log_dict[LOG_MESSAGE])
    return match.group(FIRST_MATCH) if match else None


def check_message_type(pattern, ssh_log_message):
    return re.search(pattern, ssh_log_message)


def get_message_type(ssh_log_message):
    for pattern, message_type in MESSAGE_PATTERN_DICT.items():
        if check_message_type(pattern, ssh_log_message):
            return message_type
    return OTHER_MESSAGE


if __name__ == "__main__":
    ssh_logs = get_logs_list()
    for line in ssh_logs:
        entry = parse_ssh_log(line)
        print(get_ipv4s_from_log(entry))
        print(get_user_from_log(entry))
        print(get_message_type(entry[LOG_MESSAGE]))
