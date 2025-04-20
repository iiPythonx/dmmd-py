# Copyright (c) 2025 iiPython

# Base Exceptions
class DmmDException(Exception):
    pass

class GenericInvalid(DmmDException):
    pass

# Special Exceptions
class ServerError(DmmDException):
    pass

# Specific Exceptions
class BadFile(DmmDException):
    pass

class BadJSON(DmmDException):
    pass

class InvalidData(GenericInvalid):
    pass

class InvalidName(GenericInvalid):
    pass

class InvalidTags(GenericInvalid):
    pass

class InvalidTime(GenericInvalid):
    pass

class InvalidToken(GenericInvalid):
    pass

class InvalidUUID(GenericInvalid):
    pass

class LargeSource(DmmDException):
    pass

class MissingAsset(DmmDException):
    pass

class MissingContent(DmmDException):
    pass

class UnauthorizedToken(DmmDException):
    pass

class UnsupportedMime(DmmDException):
    pass

# Map codes to exception
EXCEPTION_MAP = {
    "BAD_FILE": BadFile,
    "BAD_JSON": BadJSON,
    "INVALID_DATA": InvalidData,
    "INVALID_NAME": InvalidName,
    "INVALID_TAGS": InvalidTags,
    "INVALID_TIME": InvalidTime,
    "INVALID_TOKEN": InvalidToken,
    "INVALID_UUID": InvalidUUID,
    "LARGE_SOURCE": LargeSource,
    "MISSING_ASSET": MissingAsset,
    "MISSING_CONTENT": MissingContent,
    "UNAUTHORIZED_TOKEN": UnauthorizedToken,
    "UNSUPPORTED_MIME": UnsupportedMime
}
