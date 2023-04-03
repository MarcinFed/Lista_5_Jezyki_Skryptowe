import argparse
from lab_1 import convert_logs_to_dict
from lab_2 import parse_ssh_log, get_ipv4s_from_log, get_user_from_log, get_message_type, LOG_MESSAGE
from lab_4 import get_n_random_logs_from_random_user, calculate_ssh_global_duration_statistics, calculate_ssh_per_user_duration_statistics, get_most_least_frequent_users

READ_MODE = "r"


def parse_log():
    print(parse_ssh_log(args.log_line))
    # python lab_5.py SSH_Test.txt parse-log -l 'debug' -l 'Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2'


def ipv4s():
    converted_line = parse_ssh_log(args.log_line)
    print(get_ipv4s_from_log(converted_line))
    # python lab_5.py SSH_Test.txt ipv4s -l 'debug' -l 'Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2'
    # python lab_5.py SSH_Test.txt ipv4s -l 'Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2'


def user():
    converted_line = parse_ssh_log(args.log_line)
    print(get_user_from_log(converted_line))
    # python lab_5.py SSH_Test.txt user -l 'Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2'

def message_type():
    converted_line = parse_ssh_log(args.log_line)
    print(get_message_type(converted_line[LOG_MESSAGE]))
    # python lab_5.py SSH_Test.txt message-type -l 'Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2'


def random_logs():
    converted_logs = convert_logs_to_dict(args.log_file)
    print(get_n_random_logs_from_random_user(converted_logs, args.num_logs))
    # python lab_5.py SSH_Test.txt random-logs -n 1


def ssh_stats():
    converted_logs = convert_logs_to_dict(args.log_file)
    print(calculate_ssh_global_duration_statistics(converted_logs))
    # python lab_5.py SSH_Test.txt ssh-stats


def ssh_stats_per_user():
    converted_logs = convert_logs_to_dict(args.log_file)
    print(calculate_ssh_per_user_duration_statistics(converted_logs))
    # python lab_5.py SSH_Test.txt ssh-stats-per-user


def frequency():
    converted_logs = convert_logs_to_dict(args.log_file)
    print(get_most_least_frequent_users(converted_logs))
    # python lab_5.py SSH_Test.txt frequency


parser = argparse.ArgumentParser(description='My CLI')

parser.add_argument('log_file')

parser.add_argument('-l', '--log_level', choices=['debug', 'info', 'warning', 'error', 'critical'])

subparsers = parser.add_subparsers(title='Subcommands', dest='command')

parse_log_parser = subparsers.add_parser('parse-log')
parse_log_parser.add_argument('-l', '--log_line', help='specify log line')
parse_log_parser.set_defaults(func=parse_log)

ipv4s_parser = subparsers.add_parser('ipv4s')
ipv4s_parser.add_argument('-l', '--log_line', help='specify log line')
ipv4s_parser.set_defaults(func=ipv4s)

user_parser = subparsers.add_parser('user')
user_parser.add_argument('-l', '--log_line', help='specify log line')
user_parser.set_defaults(func=user)

message_type_parser = subparsers.add_parser('message-type')
message_type_parser.add_argument('-l', '--log_line', help='specify log line')
message_type_parser.set_defaults(func=message_type)


random_logs_parser = subparsers.add_parser('random-logs')
random_logs_parser.add_argument('-n', '--num_logs', type=int, help='specify number of logs')
random_logs_parser.set_defaults(func=random_logs)

ssh_stats_parser = subparsers.add_parser('ssh-stats')
ssh_stats_parser.set_defaults(func=ssh_stats)

ssh_stats_per_user_parser = subparsers.add_parser('ssh-stats-per-user')
ssh_stats_per_user_parser.set_defaults(func=ssh_stats_per_user)

frequency_parser = subparsers.add_parser('frequency')
frequency_parser.set_defaults(func=frequency)

args = parser.parse_args()
args.func()
