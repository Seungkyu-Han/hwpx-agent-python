class HwpxEmptyException(Exception):
    """
    Exception raised for handling empty HWPX-related content.

    This exception is intended to be used when an operation related to
    HWPX content (such as parsing or processing) encounters an empty or
    invalid value. It allows for more precise identification and handling
    of such cases.
    """

    def __init__(self, message: str):
        super().__init__(message)