def process_critical_exception(message: str):
    """Prints message, describing critical situation, and exit"""
    print(message)
    exit(1)


class NotSpecifiedIPOrPortError(Exception):
    """Error that occurs when there is not Server or Port specified in
    command-line arguments.
    """
    pass


class CanNotParseResponseError(Exception):
    """Error that occurs when we can not parse some strange
    response from RKSOK server.
    """
    pass
