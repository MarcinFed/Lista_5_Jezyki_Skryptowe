import logging, sys
from lab_2 import parse_ssh_log, get_message_type, LOG_MESSAGE, ACCEPTED_LOGGING_MESSAGE, FAILED_PASSWORD_MESSAGE, INVALID_USER_MESSAGE, DISCONNECTED_MESSAGE, FAILED_LOGGING_MESSAGE, POSSIBLE_BREAK_IN_MESSAGE
from lab_1 import get_logs_list

log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
error_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s (%(pathname)s:%(lineno)d)")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

debug_handler = logging.StreamHandler(sys.stdout)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(log_format)
debug_handler.addFilter(lambda record: record.levelno == logging.DEBUG)

info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(log_format)
info_handler.addFilter(lambda record: record.levelno == logging.INFO)

warning_handler = logging.StreamHandler(sys.stdout)
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(log_format)
warning_handler.addFilter(lambda record: record.levelno == logging.WARNING)

critical_handler = logging.StreamHandler(sys.stdout)
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(log_format)
critical_handler.addFilter(lambda record: record.levelno == logging.CRITICAL)

error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(error_format)
error_handler.addFilter(lambda record: record.levelno == logging.ERROR)


logger.addHandler(critical_handler)
logger.addHandler(error_handler)
logger.addHandler(warning_handler)
logger.addHandler(info_handler)
logger.addHandler(debug_handler)


def bytes_read_log(log_string):
    logger.debug(f"Liczba przeczytanych bajtów: {len(log_string)}")


def accepted_logging_log():
    logger.info("Udane logowanie")


def disconnected_log():
    logger.info("Zamknięcie połączenia")


def failed_logging_log():
    logger.warning("Nieudane logowanie")


def failed_password_log():
    logger.error("Błędne hasło")


def invalid_user_log():
    logger.error("Błędna nazwa użytkownika")


def possible_break_in_log():
    logger.critical("Próba włamania")


MESSAGE_LOGGING_DICT = {
    ACCEPTED_LOGGING_MESSAGE: accepted_logging_log,
    DISCONNECTED_MESSAGE: disconnected_log,
    FAILED_LOGGING_MESSAGE: failed_logging_log,
    FAILED_PASSWORD_MESSAGE: failed_password_log,
    INVALID_USER_MESSAGE: invalid_user_log,
    POSSIBLE_BREAK_IN_MESSAGE: possible_break_in_log,
}


def process_log_line(log):
    parsed_log = parse_ssh_log(log)
    message_type = get_message_type(parsed_log[LOG_MESSAGE])
    bytes_read_log(log)

    for message, action in MESSAGE_LOGGING_DICT.items():
        if message_type == message:
            return action()


def process_logs():
    for log in get_logs_list():
        process_log_line(log)


if __name__ == "__main__":
    process_logs()


