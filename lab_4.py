import statistics, random
from datetime import datetime
from lab_1 import get_logs_dict
from lab_2 import get_user_from_log, get_message_type, LOG_MESSAGE, ACCEPTED_LOGGING_MESSAGE, DISCONNECTED_MESSAGE, get_ipv4s_from_log
from tools import LOG_TIMESTAMP


UNKNOWN_USER = "unknown"
NO_USER_INFO = None
DATE_FORMAT = "%b %d %H:%M:%S"
USERNAME_TOUPLE_PLACE = 0
IPV4_TOUPLE_PLACE = 1
FIRST_IPV4_FROM_LOG = 0


def is_login(log):
    message_type = get_message_type(log)
    return message_type == ACCEPTED_LOGGING_MESSAGE


def get_all_users(logs):
    users = []
    for log in logs:
        user = get_user_from_log(log)
        if user != NO_USER_INFO and user != UNKNOWN_USER:
            users.append(user)
    return users


def get_all_accepted_users(logs):
    users = []
    for log in logs:
        if is_login(log):
            user = get_user_from_log(log)
            if user is not NO_USER_INFO and user != UNKNOWN_USER:
                users.append(user)
    return users


def unique_users_filter(users):
    users = list(set(users))
    return users


def get_logs_for_user(logs, user):
    user_logs = []
    for log in logs:
        if user == get_user_from_log(log):
            user_logs.append(log)
    return user_logs


def get_n_random_logs_from_random_user(logs, n):
    user = random.choice(unique_users_filter(get_all_users(logs)))
    user_logs = get_logs_for_user(logs, user)
    return random.sample(user_logs, n if n < len(user_logs) else len(user_logs))


def count_users_instances(users):
    count_users = {}
    for user in users:
        if user in count_users:
            count_users[user] += 1
        else:
            count_users[user] = 1
    return count_users


def get_max_instances_users(count_users):
    max_instances_users = []
    max_value = max(count_users.values())
    for key, value in count_users.items():
        if value == max_value:
            max_instances_users.append(key)
    return max_instances_users


def get_min_instances_users(count_users):
    min_instances_users = []
    min_value = min(count_users.values())
    for key, value in count_users.items():
        if value == min_value:
            min_instances_users.append(key)
    return min_instances_users


def get_most_least_frequent_users(logs):
    users = get_all_accepted_users(logs)
    count_users = count_users_instances(users)
    max_instances_users = get_max_instances_users(count_users)
    min_instances_users = get_min_instances_users(count_users)
    return max_instances_users, min_instances_users


def find_connection_close_log(log, logs_to_find):
    user_ip = get_ipv4s_from_log(log)
    for log in logs_to_find:
        if get_ipv4s_from_log(log) == user_ip and get_message_type(log) == DISCONNECTED_MESSAGE:
            return log


def calculate_connection_duration(log, logs):
    log_index = logs.index(log)
    logs_to_find = logs[log_index:]

    found_log = find_connection_close_log(log, logs_to_find)

    if found_log is None:
        return None

    start_time = datetime.strptime(log[LOG_TIMESTAMP], DATE_FORMAT)
    end_time = datetime.strptime(found_log[LOG_TIMESTAMP], DATE_FORMAT)

    return (end_time - start_time).total_seconds()


def calculate_session_times(logs):
    ssh_session_durations = []
    for log in logs:
        if get_message_type(log) == ACCEPTED_LOGGING_MESSAGE:
            connection_duration = calculate_connection_duration(log, logs)
            if connection_duration is not None:
                ssh_session_durations.append(connection_duration)
    return ssh_session_durations


def calculate_ssh_global_duration_statistics(logs):
    ssh_session_durations = calculate_session_times(logs)
    if len(ssh_session_durations) > 1:
        duration_mean = statistics.mean(ssh_session_durations)
        std_dev = statistics.stdev(ssh_session_durations)
        return duration_mean, std_dev
    elif len(ssh_session_durations) == 1:
        return ssh_session_durations[0], 0
    else:
        return None


def calculate_ssh_per_user_duration_statistics(logs):
    users_statistics = {}
    users = []
    for log in logs:
        if len(get_ipv4s_from_log(log)) > 0 and get_user_from_log(log) is not None:
            users.append((get_user_from_log(log), get_ipv4s_from_log(log)[FIRST_IPV4_FROM_LOG]))
    for user in users:
        user_logs = [log for log in logs if len(get_ipv4s_from_log(log)) > 0 and get_ipv4s_from_log(log)[FIRST_IPV4_FROM_LOG] == user[IPV4_TOUPLE_PLACE]]
        users_statistics[user[USERNAME_TOUPLE_PLACE]] = calculate_ssh_global_duration_statistics(user_logs)
    return users_statistics


if __name__ == '__main__':
    logs = get_logs_dict()
    print(get_n_random_logs_from_random_user(logs, 3))
    print(get_most_least_frequent_users(logs))
    print(calculate_ssh_global_duration_statistics(logs))
    print(calculate_ssh_per_user_duration_statistics(logs))
