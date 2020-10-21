from common import *

# 1) Communication section

# Create a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to 127.0.0.1:12345
s.connect(('127.0.0.1', 12345))

while True:

    # Waiting for a message for Bob
    next_m_key = get_next_m_key(m)
    if next_m_key == None:
        break

    m_out = input(next_m_key + '> ')
    if m_out == 'q':
        break

    m[next_m_key] = m_out
    s.send(m_out.encode('utf-8'))

    # Waiting for a message from Bob
    next_m_key = get_next_m_key(m)
    if next_m_key == None:
        break

    m_in = s.recv(1024).decode('utf-8')
    if not m_in:
        break

    m[next_m_key] = m_in
    print('Bob sent ' + next_m_key + ': ' + m_in)

# Close the coonection with Bob
s.close()

# 2) Postprocessing section

# Extract information from messages

# Verify signatures

# Compute output of the dice
a = binary_string_to_int(m['a,r + sig'][0:3])
b = binary_string_to_int(m['b + sig'][0:3])
d = (a ^ b) % 6 + 1
print('Compute d = (a ^ b) % 6 + 1: ' + str(a) + ' ^ ' + str(b) + ' % 6 + 1 = ' + str(d))
