# -*- coding: utf-8 -*-
############################################################################
# Commons.py                                                               #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2021          #
############################################################################

"""
TODO: ...
"""

############################################################################
# Singleton ################################################################
"""
Usage:
    class X (metaclass=Singleton):
        pass
"""
############################################################################
class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


############################################################################
# Digest ###################################################################
"""
Usage:
    TODO:

"""
############################################################################
class Digest (object):
    def __init__ (self, secret):
        self.__secret = secret.encode('utf-8')

    def __call__ (self, data):
        import base64
        import hashlib
        import hmac

        digest_maker = hmac.new(self.__secret,
                                data.encode('utf-8'),
                                hashlib.sha256)
        return base64.encodestring(digest_maker.digest()).decode('utf-8').rstrip()


############################################################################
# MyIP #####################################################################
"""
Usage:
    TODO:

"""
############################################################################
def MyIP ():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = 'x.x.x.x'
    finally:
        s.close()
    return IP


# eof #

