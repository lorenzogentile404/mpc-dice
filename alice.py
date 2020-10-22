from common import *

# 1) Communication

# Create a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to TCP_IP:TCP_PORT
s.connect((TCP_IP, TCP_PORT))

# 1.1) Preprocessing

a = input('a > ')
r = str(random.getrandbits(k_com))
c = com(a, r)
m['com(a,r) sig'] = {'message': sig_m(c, 'Alice'), 'alreadyTransmitted': False} # A -> B
m['a r sig'] = {'message': sig_m(a + ' ' + r, 'Alice'), 'alreadyTransmitted': False} # A -> B

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

    m_in = s.recv(BUFFER_SIZE).decode('utf-8')
    print('Bob sent: ' + next_m_key + ' = ' + print_sig_m(next_m_key, m_in))
    m[next_m_key] = {'message': m_in, 'alreadyTransmitted': True}

# Close the coonection with Bob
s.close()

# 2) Postprocessing

# Extract information from messages
b = m['b sig']['message'].split()[0]

# Verify signatures
assert(verify_sig(b , 'Bob', extract_sig('b sig', m['b sig']['message'])))
print('\nb sig valid.\n')

# Compute output of the dice
compute_output(a, b)
