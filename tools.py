import re

LOG_PATTERN = r"(\w{3}\s+\d+\s\d+:\d+:\d+)\s(\w+)\ssshd\[\d+\]:\s([^\n]+)"
LOG_MESSAGE = "message"
LOG_HOSTNAME = "hostname"
LOG_TIMESTAMP = "timestamp"

def parse_ssh_log(log_string):
    for match in re.finditer(LOG_PATTERN, log_string):
        timestamp, hostname, message = match.groups()
        ssh_log_dict = {
            LOG_TIMESTAMP: timestamp,
            LOG_HOSTNAME: hostname,
            LOG_MESSAGE: message
        }
    return ssh_log_dict