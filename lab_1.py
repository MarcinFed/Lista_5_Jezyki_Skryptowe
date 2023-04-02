from tools import parse_ssh_log

READ_MODE = "r"


def convert_logs_to_array(filename):
    with open(filename, READ_MODE) as f:
        lines = f.readlines()
    return [line for line in lines]


def convert_logs_to_dict(filename):
    logs_array = convert_logs_to_array(filename)
    return [parse_ssh_log(log) for log in logs_array]


def get_logs_list():
    return convert_logs_to_array('SSH_Test.txt')


def get_logs_dict():
    return convert_logs_to_dict('SSH_Test.txt')
