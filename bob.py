import socket
import collections

# Support function to get the key of the next expected message
def get_next_m_key(m):
    return ([key for key, value in m.items() if value == None] + [None])[0]

# Support function to convert a binary string to int
def binary_string_to_int(m):
    return sum([int(b)*2**p for b,p in zip(m, range(len(m) - 1,-1,-1))])

def bob():

    # Protocol messages
    m = collections.OrderedDict()
    m['com(a|r) + sig'] = None # A -> B
    m['b + sig'] = None # A <- B
    m['a,r + sig'] = None # A -> B

    # Create a TCP socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the port 12345 and listen to requests coming from 127.0.0.1
    s.bind(('127.0.0.1', 12345))
    s.listen(1)

    # Establish connection with Alice
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    while True:

        # Waiting for a message from Alice
        next_m_key = get_next_m_key(m)
        if next_m_key == None:
            break

        m_in = c.recv(1024).decode('utf-8')
        if not m_in:
            break

        m[next_m_key] = m_in
        print('Alice sent ' + next_m_key + ': ' + m_in)

        # Waiting for a message for Alice
        next_m_key = get_next_m_key(m)
        if next_m_key == None:
            break

        m_out = input(next_m_key + '> ')
        if m_out == 'q':
            break

        m[next_m_key] = m_out
        c.send(m_out.encode('utf-8'))

    # Close connection with Alice
    c.close()

    # Show collected messages
    print(m)

    # Extract information from messages

    # Verify signatures

    # Compute output of the dice
    a = binary_string_to_int(m['a,r + sig'][0:3])
    b = binary_string_to_int(m['b + sig'][0:3])
    d = (a ^ b) % 6 + 1
    print('Compute d = (a ^ b) % 6 + 1: ' + bin(a) + ' ^ ' + bin(b) + ' % 6 + 1 = ' + bin(d))

if __name__ == '__main__':
    bob()
