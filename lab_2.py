import re, sys

LOG_PATTERN = r"(\w{3}\s+\d+\s\d+:\d+:\d+)\s(\w+)\ssshd\[\d+\]:\s([^\n]+)"
IPV4_PATTERN = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
USER_NAME_PATTERN = r"user\s(\w+)"
LOG_MESSAGE = "message"
LOG_HOSTNAME = "hostname"
LOG_TIMESTAMP = "timestamp"
FIRST_MATCH = 1
ACCEPTED_LOGGING_MESSAGE_PATTERN = r"Accepted.*for"
FAILED_PASSWORD_MESSAGE_PATTERN = r"Failed.*password"
INVALID_USER_MESSAGE_PATTERN = r"Failed.*invalid user"
DISCONNECTED_MESSAGE_PATTERN = r"Disconnected from"
FAILED_LOGGING_MESSAGE_PATTERN = r"Failed.*from"
POSSIBLE_BREAK_IN_MESSAGE_PATTERN = r"POSSIBLE BREAK-IN ATTEMPT"
ACCEPTED_LOGGING_MESSAGE = "udane logowanie"
FAILED_PASSWORD_MESSAGE = "błędne hasło"
INVALID_USER_MESSAGE = "błędna nazwa użytkownika"
DISCONNECTED_MESSAGE = "zamknięcie połączenia"
FAILED_LOGGING_MESSAGE = "nieudane logowanie"
POSSIBLE_BREAK_IN_MESSAGE = "próba włamania"
OTHER_MESSAGE = "inne"
MESSAGE_PATTERN_DICT = {
    ACCEPTED_LOGGING_MESSAGE_PATTERN : ACCEPTED_LOGGING_MESSAGE,
    FAILED_LOGGING_MESSAGE_PATTERN : FAILED_LOGGING_MESSAGE,
    FAILED_PASSWORD_MESSAGE_PATTERN : FAILED_PASSWORD_MESSAGE,
    DISCONNECTED_MESSAGE_PATTERN : DISCONNECTED_MESSAGE,
    INVALID_USER_MESSAGE_PATTERN : INVALID_USER_MESSAGE,
    POSSIBLE_BREAK_IN_MESSAGE_PATTERN : POSSIBLE_BREAK_IN_MESSAGE,
}


def parse_ssh_log(log_string):
    for match in re.finditer(LOG_PATTERN, log_string):
        timestamp, hostname, message = match.groups()
        ssh_log_dict = {
            LOG_TIMESTAMP: timestamp,
            LOG_HOSTNAME: hostname,
            LOG_MESSAGE: message
        }
    return ssh_log_dict


def get_ipv4s_from_log(ssh_log_dict):
    ipv4_regex = re.compile(IPV4_PATTERN)
    ipv4s = ipv4_regex.findall(ssh_log_dict[LOG_MESSAGE])
    return ipv4s


def get_user_from_log(ssh_log_dict):
    match = re.search(USER_NAME_PATTERN, ssh_log_dict[LOG_MESSAGE])
    return match.group(FIRST_MATCH) if match else None


def get_message_type(ssh_log_message):
    for message_pattern, message in MESSAGE_PATTERN_DICT.items():
        if re.search(message_pattern, ssh_log_message):
            return message
    return OTHER_MESSAGE


if __name__ == "__main__":
    print(parse_ssh_log(sys.stdin))
    sys.stdin.close()
