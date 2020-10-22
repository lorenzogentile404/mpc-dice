from common import *

# 1) Communication

# Create a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the port 12345 and listen to requests coming from 127.0.0.1
s.bind(('127.0.0.1', 12345))
s.listen(1)

# Establish connection with Alice
c, addr = s.accept()
print('Connection from: ' + str(addr))

# 1.1) Preprocessing

b = input('b > ')
m['b sig'] = {'message': format_sig_m(b,'Bob'), 'alreadyTransmitted': False} # A <- B

while True:

    # Waiting for a message from Alice
    next_m_key = get_next_m_key(m)
    if next_m_key == None:
        break

    m_in = c.recv(1024).decode('utf-8')
    print('Alice sent: ' + next_m_key + ' = \n' + m_in.replace(' ', '\n\n', next_m_key.count(' ')) + '\n\n')
    m[next_m_key] = {'message': m_in, 'alreadyTransmitted': True}

    # Waiting for a message for Alice
    next_m_key = get_next_m_key(m)
    if next_m_key == None:
        break

    m_out = input('Press enter to send: ' + next_m_key + ' > ') or m[next_m_key]['message']
    c.send(m_out.encode('utf-8'))
    m[next_m_key] = {'message': m_out, 'alreadyTransmitted': True}

# Close connection with Alice
c.close()

# 2) Postprocessing

# Extract information from messages
c = m['com(a,r) sig']['message'].split()[0]
a = m['a r sig']['message'].split()[0]
r = m['a r sig']['message'].split()[1]

# Verify signatures
assert(verify_sig(c , 'Alice', m['com(a,r) sig']['message'].replace(c + ' ','', 1)))
print('\ncom(a|r) sig valid.\n')

assert(verify_sig(a + ' ' + r, 'Alice', m['a r sig']['message'].replace(a + ' ' + r + ' ','', 1)))
print('\na r sig valid.\n')

# Verify commitment
assert(verify_com(a,r,c))
print('\ncom(a,r) valid.\n')

# Compute output of the dice
d = (binary_string_to_int(a) ^ binary_string_to_int(b)) % 6 + 1
print('Compute d = (a ^ b) % 6 + 1: ' + str(a) + ' ^ ' + str(b) + ' % 6 + 1 = ' + str(d))
