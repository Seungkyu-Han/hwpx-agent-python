class AgentConfigException(Exception):
    """
    Exception raised for errors in the agent configuration.

    This class is used to represent exceptions related to agent configuration
    issues. It inherits from the built-in Exception class and includes an
    additional message parameter to provide details about the specific error.
    """

    def __init__(self, message: str):
        super().__init__(message)