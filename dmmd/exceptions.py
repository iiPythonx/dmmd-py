# Copyright (c) 2025 iiPython

# Global shared exception class
class DmmDException(Exception):
    pass

# Special exceptions
class BadRequest(DmmDException):
    pass

class NotFound(DmmDException):
    pass

class ServerError(DmmDException):
    pass
