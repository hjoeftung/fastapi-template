from structlog import get_logger

request_logger = get_logger("requests")
exception_logger = get_logger("exceptions")
