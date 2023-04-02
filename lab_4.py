import statistics, random, datetime
from lab_2 import get_user_from_log, LOG_MESSAGE

UNKNOWN_USER = "unknown"
NO_USER_INFO = None


def get_all_users(logs):
    users = []
    for log in logs:
        user = get_user_from_log(log[LOG_MESSAGE])
        if user is not NO_USER_INFO and user != UNKNOWN_USER:
            users.append(user)
    return users


def unique_users_filter(users):
    users = list(set(users))
    return users


def get_logs_for_user(logs, user):
    user_logs = []
    for log in logs:
        if user == get_user_from_log(log[LOG_MESSAGE]):
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
    users = get_all_users(logs)
    count_users = count_users_instances(users)
    max_instances_users = get_max_instances_users(count_users)
    min_instances_users = get_min_instances_users(count_users)
    return max_instances_users, min_instances_users


