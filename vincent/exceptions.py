"""custom exceptions for vincent analysis"""
class VincentException(Exception):
    """base exception for vincent project"""

class MissingAuthentication(VincentException):
    """expected authentication keys for service"""


class VincentWarning(Warning):
    """base warning for vincent project"""
