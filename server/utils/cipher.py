"""Cipher
"""

from binascii import b2a_hex, a2b_hex, Error
import Crypto.Cipher.AES as AES


def set_length(data, length):
    """set length for key
    """
    datalen = len(data)
    if datalen < length:
        data = data + (b'\0' * (length - datalen))
    return data[:length]


class AESCipher:
    """AES Cipher
    """

    def __init__(self, key, mode, iv):
        self.key = bytes(key, encoding='utf-8')
        self.mode = mode
        self.iv_key = bytes(iv, encoding='utf-8')

        self.key = set_length(self.key, 32)
        self.iv_key = set_length(self.iv_key, 16)

    def make_cryptor(self):
        """make cryptor
        """
        return AES.new(self.key, self.mode, self.iv_key)

    def encrypt(self, text):
        """encrypt
        """
        cryptor = self.make_cryptor()
        text = bytes(text, encoding='utf-8')
        length = len(text)
        if length % 16 != 0:
            text = text + (b'\0' * (16 - length % 16))

        return b2a_hex(cryptor.encrypt(text)).decode('utf-8')

    def decrypt(self, text):
        """decrypt
        """
        cryptor = self.make_cryptor()
        text = bytes(text, encoding='utf-8')
        try:
            text = a2b_hex(text)
            text = cryptor.decrypt(text)
            text = text.rstrip(b'\0')
            return text.decode('utf-8')
        except Error:
            return None
        except UnicodeDecodeError:
            return None
        except ValueError:
            return None
        else:
            return None
        return None

AESCipher.cipher = AESCipher('Q2UKvCVZZBj655AI7wVUuj8jE4oiaiLn', AES.MODE_CBC, 'x3qqbVLE4XAGW9RI')

def decrypt(text):
    """decrypt
    """
    if text is None:
        return None
    return AESCipher.cipher.decrypt(text)
