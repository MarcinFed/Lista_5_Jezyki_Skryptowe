import re, sys
from lab_3 import bytes_read_log, accepted_logging_log, disconnected_log, failed_logging_log, failed_password_log, invalid_user_log, possible_break_in_log, logger


LOG_PATTERN = r"(\w{3}\s+\d+\s\d+:\d+:\d+)\s(\w+)\ssshd\[\d+\]:\s([^\n]+)"
IPV4_PATTERN = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
USER_NAME_PATTERN = r"user\s(\w+)"
LOG_MESSAGE = "message"
LOG_HOSTNAME = "hostname"
LOG_TIMESTAMP = "timestamp"
FIRST_MATCH = 1
ACCEPTED_LOGGING_MESSAGE_PATTERN = r"Accepted.*for"
FAILED_PASSWORD_MESSAGE_PATTERN = r"Failed.*password"
INVALID_USER_MESSAGE_PATTERN = r"(?i)nvalid user"
DISCONNECTED_MESSAGE_PATTERN = r"Connection closed"
FAILED_LOGGING_MESSAGE_PATTERN = r"Failed.*from"
POSSIBLE_BREAK_IN_MESSAGE_PATTERN = r"POSSIBLE BREAK-IN ATTEMPT"
ACCEPTED_LOGGING_MESSAGE = "udane logowanie"
FAILED_PASSWORD_MESSAGE = "błędne hasło"
INVALID_USER_MESSAGE = "błędna nazwa użytkownika"
DISCONNECTED_MESSAGE = "zamknięcie połączenia"
FAILED_LOGGING_MESSAGE = "nieudane logowanie"
POSSIBLE_BREAK_IN_MESSAGE = "próba włamania"
OTHER_MESSAGE = "inne"


def accepted_logging_notice():
    accepted_logging_log()
    return ACCEPTED_LOGGING_MESSAGE


def failed_password_notice():
    failed_password_log()
    return FAILED_PASSWORD_MESSAGE


def disconnected_notice():
    disconnected_log()
    return DISCONNECTED_MESSAGE


def invalid_user_notice():
    invalid_user_log()
    return INVALID_USER_MESSAGE


def possible_break_in_notice():
    possible_break_in_log()
    return POSSIBLE_BREAK_IN_MESSAGE


def failed_logging_notice():
    failed_logging_log()
    return FAILED_LOGGING_MESSAGE


MESSAGE_PATTERN_DICT = {
    ACCEPTED_LOGGING_MESSAGE_PATTERN: accepted_logging_notice,
    FAILED_PASSWORD_MESSAGE_PATTERN: failed_password_notice,
    DISCONNECTED_MESSAGE_PATTERN: disconnected_notice,
    INVALID_USER_MESSAGE_PATTERN: invalid_user_notice,
    POSSIBLE_BREAK_IN_MESSAGE_PATTERN: possible_break_in_notice,
    FAILED_LOGGING_MESSAGE_PATTERN: failed_logging_notice,
}


def parse_ssh_log(log_string):
    for match in re.finditer(LOG_PATTERN, log_string):
        timestamp, hostname, message = match.groups()
        ssh_log_dict = {
            LOG_TIMESTAMP: timestamp,
            LOG_HOSTNAME: hostname,
            LOG_MESSAGE: message
        }
    bytes_read_log(log_string)
    return ssh_log_dict


def get_ipv4s_from_log(ssh_log_dict):
    ipv4_regex = re.compile(IPV4_PATTERN)
    ipv4s = ipv4_regex.findall(ssh_log_dict[LOG_MESSAGE])
    return ipv4s


def get_user_from_log(ssh_log_dict):
    match = re.search(USER_NAME_PATTERN, ssh_log_dict[LOG_MESSAGE])
    return match.group(FIRST_MATCH) if match else None


def get_message_type(ssh_log_message):
    for message_pattern, action in MESSAGE_PATTERN_DICT.items():
        if re.search(message_pattern, ssh_log_message):
            return action()
    return OTHER_MESSAGE


if __name__ == "__main__":
    ssh_logs_file = open("SSH_Test.txt", "r")
    for line in ssh_logs_file:
        parse = parse_ssh_log(line)
        print(get_message_type(parse[LOG_MESSAGE]))
