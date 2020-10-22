from common import *

# 1) Communication

# Create a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to 127.0.0.1:12345
s.connect(('127.0.0.1', 12345))

# 1.1) Preprocessing

a = input('a > ')
r = str(random.getrandbits(1024))
c = com(a, r)
m['com(a,r) sig'] = {'message': format_sig_m(c, 'Alice'), 'alreadyTransmitted': False} # A -> B
m['a r sig'] = {'message': format_sig_m(a + ' ' + r, 'Alice'), 'alreadyTransmitted': False} # A -> B

while True:

    # Waiting for a message for Bob
    next_m_key = get_next_m_key(m)
    if next_m_key == None:
        break

    m_out = input('Press enter to send: ' + next_m_key + ' > ') or m[next_m_key]['message']
    s.send(m_out.encode('utf-8'))
    m[next_m_key] = {'message': m_out, 'alreadyTransmitted': True}

    # Waiting for a message from Bob
    next_m_key = get_next_m_key(m)
    if next_m_key == None:
        break

    m_in = s.recv(1024).decode('utf-8')
    print('Bob sent: ' + next_m_key + ' = \n' + m_in.replace(' ', '\n\n', next_m_key.count(' ')) + '\n\n')
    m[next_m_key] = {'message': m_in, 'alreadyTransmitted': True}

# Close the coonection with Bob
s.close()

# 2) Postprocessing

# Extract information from messages
b = m['b sig']['message'].split()[0]

# Verify signatures
assert(verify_sig(b , 'Bob', m['b sig']['message'].replace(b + ' ','', 1)))
print('\nb sig valid.\n')

# Compute output of the dice
d = (binary_string_to_int(a) ^ binary_string_to_int(b)) % 6 + 1
print('Compute d = (a ^ b) % 6 + 1: ' + str(a) + ' ^ ' + str(b) + ' % 6 + 1 = ' + str(d))
