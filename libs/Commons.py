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


############################################################################
# Display1306 ##############################################################
"""
Usage:
    TODO:


"""
############################################################################
class Display1306 (object):
    """ ### Packages you might need to install ###
        # sudo apt-get install libjpeg8-dev -y
        # sudo pip3 install Pillow
    """
    from actuators.SSD1306 import SSD1306
    def __init__ (self, address=SSD1306.I2C_BASE_ADDRESS, lock=None):
        from PIL import Image
        from PIL import ImageDraw
        from PIL import ImageFont

        if lock != None:
            self.lock = lock
        else:
            import threading
            self.lock = threading.Lock()

        self.display = self.SSD1306(address) # todo: check if 'with lock' is needed
        self.display.begin()
        self.off()

        self.xpos = 4
        self.ypos = 2
        self.image = Image.new('1', (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        (_, self.textheight) = self.draw.textsize("Text", font=self.font)

    def print (self, line1="", line2="", line3="", line4="", line5=""):
        lines = [line1, line2, line3, line4, line5]
        y = self.ypos

        with self.lock:
            self.draw.rectangle((0,0,self.display.width,self.display.height), outline=0, fill=255)
            for line in lines:
                self.draw.text((self.xpos, y), line)
                y += self.textheight

            self.display.image(self.image)
            self.display.display()

    def off (self):
        with self.lock:
            self.display.clear()
            self.display.display()


# eof #

