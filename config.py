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
    INCORRECT_REQUEST = "НИПОНЯЛ"


PROTOCOL = "РКСОК/1.0"
ENCODING = "UTF-8"