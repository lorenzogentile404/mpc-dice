from common import *

# 1) Communication

# Create a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the port TCP_PORT and listen to requests coming from TCP_IP
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# Establish connection with Alice
c, addr = s.accept()
print('Connection from: ' + str(addr))

# 1.1) Preprocessing

b = input('b > ')
m['b sig'] = {'message': sig_m(b,'Bob'), 'alreadyTransmitted': False} # A <- B

while True:

    # Waiting for a message from Alice
    next_m_key = get_next_m_key(m)
    if next_m_key == None:
        break

    m_in = c.recv(BUFFER_SIZE).decode('utf-8')
    print('Alice sent: ' + next_m_key + ' = ' + print_sig_m(next_m_key, m_in))
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

# Verify commitment
assert(verify_com(a,r,c))
print('\ncom(a,r) valid.\n')

# Verify signatures
assert(verify_sig(c , 'Alice', extract_sig('com(a,r) sig', m['com(a,r) sig']['message'])))
print('\ncom(a|r) sig valid.\n')

assert(verify_sig(a + ' ' + r, 'Alice', extract_sig('a r sig', m['a r sig']['message'])))
print('\na r sig valid.\n')

# Compute output of the dice
compute_output(a, b)
