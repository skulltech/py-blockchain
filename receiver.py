from socket import *


while True:
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 5000))
	m = s.recvfrom(1024)
	print('[*] Received data from {m[1]}: {m[0]}'.format(m=m))
