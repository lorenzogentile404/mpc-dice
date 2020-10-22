import socket
import collections

# Support function to get the key of the next expected message
def get_next_m_key(m):
    return ([key for key, value in m.items() if value["alreadyTransmitted"] == False] + [None])[0]

# Support function to convert a binary string to int
def binary_string_to_int(m):
    return sum([int(b)*2**p for b,p in zip(m, range(len(m) - 1, -1, -1))])

# Protocol messages
m = collections.OrderedDict()

m['com(a,r) sig'] = {"message": None, "alreadyTransmitted": False} # A -> B
m['b sig'] = {"message": None, "alreadyTransmitted": False} # A <- B
m['a r sig'] = {"message": None, "alreadyTransmitted": False} # A -> B

# https://pycryptodome.readthedocs.io/en/latest/src/hash/sha256.html
from Crypto.Hash import SHA256
from Crypto.Random import random

def com(m, r):
    h = SHA256.new()
    h.update(bytes(m + r, 'utf-8'))
    return h.hexdigest()

def verify_com(m, r, c):
    return com(m, r) == c

# https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
from Crypto.PublicKey import RSA

#def generateKeyPair(name):
#    privatekey = RSA.generate(2048)
#    f_private = open('privatekey_' + name + '.pem','wb')
#    f_private.write(privatekey.export_key('PEM'))
#    f_private.close()

#    publickey = privatekey.publickey()
#    f_public = open('publickey_' + name + '.pem','wb')
#    f_public.write(publickey.export_key('PEM'))
#    f_public.close()

# generateKeyPair('Alice')
# generateKeyPair('Bob')

# https://www.pycryptodome.org/en/latest/src/signature/pkcs1_v1_5.html
from Crypto.Signature import pkcs1_15

def sig(m, name):
    f = open('privatekey_' + name + '.pem','r')
    privatekey = RSA.import_key(f.read())
    f.close()

    m = bytes(m, 'utf-8')
    h = SHA256.new(m)
    return pkcs1_15.new(privatekey).sign(h)

def verify_sig(m, name, s):
    s = s.encode('latin-1')

    f = open('publickey_' + name + '.pem','r')
    publickey = RSA.import_key(f.read())
    f.close()

    m = bytes(m, 'utf-8')
    h = SHA256.new(m)
    try:
        pkcs1_15.new(publickey).verify(h, s)
        return True
    except (ValueError, TypeError):
        return False

def format_sig_m(m, name):
    return m + ' ' + sig(m, name).decode('latin-1')
