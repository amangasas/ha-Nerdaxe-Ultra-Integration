class NerdaxeError(Exception):
    pass


class NerdaxeConnectionError(NerdaxeError):
    pass


class NerdaxeAuthError(NerdaxeError):
    pass