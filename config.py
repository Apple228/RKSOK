from enum import Enum


class RequestVerb(Enum):
    """Verbs specified in RKSOK specs for requests."""

    GET = "ОТДОВАЙ"
    DELETE = "УДОЛИ"
    WRITE = "ЗОПИШИ"


class ResponseStatus(Enum):
    """Response statuses specified in RKSOK specs for responses."""

    OK = "НОРМАЛДЫКС"
    NOTFOUND = "НИНАШОЛ"
    NOT_APPROVED = "НИЛЬЗЯ"
    APPROVED = "МОЖНА"
    INCORRECT_REQUEST = "НИПОНЯЛ"


PROTOCOL = "РКСОК/1.0"
ENCODING = "UTF-8"
VALIDATION_SERVER_URL = "vragi-vezde.to.digital"
VALIDATION_SERVER_PORT = 51624

DB_DIR = "db"