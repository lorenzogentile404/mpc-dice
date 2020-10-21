import socket
import collections

# Support function to get the key of the next expected message
def get_next_m_key(m):
    return ([key for key, value in m.items() if value == None] + [None])[0]

# Support function to convert a binary string to int
def binary_string_to_int(m):
    return sum([int(b)*2**p for b,p in zip(m, range(len(m) - 1,-1,-1))])

# Protocol messages
m = collections.OrderedDict()
m['com(a|r) + sig'] = None # A -> B
m['b + sig'] = None # A <- B
m['a,r + sig'] = None # A -> B
