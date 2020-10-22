import socket
import collections

# Security parameters
k_RSA = 2048 # Signatures
k_com = 1024 # Commitment

# Communication parameters

# https://wiki.python.org/moin/TcpCommunication
TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024

# Protocol messages and flag indicating if the message has already been transmitted
m = collections.OrderedDict()

m['com(a,r) sig'] = {"message": None, "alreadyTransmitted": False} # A -> B
m['b sig'] = {"message": None, "alreadyTransmitted": False} # A <- B
m['a r sig'] = {"message": None, "alreadyTransmitted": False} # A -> B

# Support function to get the key of the next expected message
def get_next_m_key(m):
    return ([key for key, value in m.items() if value["alreadyTransmitted"] == False] + [None])[0]

# Commitment

# https://pycryptodome.readthedocs.io/en/latest/src/hash/sha256.html
from Crypto.Hash import SHA256
from Crypto.Random import random

def com(m, r):
    h = SHA256.new()
    h.update(bytes(m + r, 'utf-8'))
    return h.hexdigest()

def verify_com(m, r, c):
    return com(m, r) == c

# Generate RSA key pair

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

# Signature

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

# Support function to sign and format a message
def sig_m(m, name):
    return m + ' ' + sig(m, name).decode('latin-1')

# Support function to print nicely a signed message
def print_sig_m(key, m):
    p = '\n\n' + m.split()[0]
    if key.count(' ') > 1:
        p += '\n\n' + m.split()[1]
    s = extract_sig(key, m)
    p += '\n\n' + str(s.encode('latin-1')) + '\n\n'
    return p

# Support function to extract signature from a signed message
# structured as field1 optional_field2 sig
def extract_sig(key, m):
    before_sig = m.split()[0] + ' '
    if key.count(' ') > 1:
        before_sig = m.split()[0] + ' ' + m.split()[1] + ' '
    s = m.replace(before_sig, '', 1)
    return s

# Support function to convert a binary string to int
def binary_string_to_int(m):
    return sum([int(b)*2**p for b,p in zip(m, range(len(m) - 1, -1, -1))])

# Compute output and print it nicely
def compute_output(a, b):
    # Compute
    a_xor_b = binary_string_to_int(a) ^ binary_string_to_int(b)
    d = a_xor_b % 6 + 1

    # Print steps
    print('Compute d = (a ^ b) % 6 + 1')
    print( a + ' ^ ' + b + ' = ' + ''.join(['1' if i!=j else '0' for i,j in zip(a, b)]) + ' = ' + str(a_xor_b) + ' (base 10)')
    print(str(a_xor_b) + ' % 6 + 1 = ' + str(d))
