# Copyright (c) 2025 iiPython

# Base Exceptions
class DmmDException(Exception):
    pass

class GenericInvalid(DmmDException):
    pass

class UnauthorizedToken(DmmDException):
    pass

# Special Exceptions
class ServerException(DmmDException):
    pass

class UnknownException(DmmDException):
    pass

# Exceptions / iCDN
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

class UnsupportedMime(DmmDException):
    pass

# Exceptions / Static
class MissingEndpoint(DmmDException):
    pass

class RouteAbort(DmmDException):
    pass

class ServerFailure(DmmDException):
    pass

# Map codes to exception
EXCEPTION_MAP = {

    # Base
    "UNAUTHORIZED_TOKEN": UnauthorizedToken,
    "SERVER_EXCEPTION"  : ServerException,
    "UNKNOWN_EXCEPTION" : UnknownException,

    # iCDN (https://github.com/DmmDGM/dmmd-icdn/blob/main/src/except.ts#L3-L18)
    "BAD_FILE"          : BadFile,
    "BAD_JSON"          : BadJSON,
    "INVALID_DATA"      : InvalidData,
    "INVALID_NAME"      : InvalidName,
    "INVALID_TAGS"      : InvalidTags,
    "INVALID_TIME"      : InvalidTime,
    "INVALID_TOKEN"     : InvalidToken,
    "INVALID_UUID"      : InvalidUUID,
    "LARGE_SOURCE"      : LargeSource,
    "MISSING_ASSET"     : MissingAsset,
    "MISSING_CONTENT"   : MissingContent,
    "UNSUPPORTED_MIME"  : UnsupportedMime,

    # Static (https://github.com/dmmd-servers/static-cdn/blob/main/core/faults.ts#L11-L28)
    "MISSING_ENDPOINT"  : MissingEndpoint,
    "ROUTE_ABORT"       : RouteAbort,
    "SERVER_FAILURE"    : ServerFailure,
}
