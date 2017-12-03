import socket
import zlib


def getdata(message):
	length = len(message)

	if len(str(length)) > 16:
		raise Exception('The message is too long! Exiting')

	data = '{:>16}'.format(str(length)).encode('UTF-8') + '{:>10}'.format(str(zlib.crc32(message))).encode('UTF-8') + message
	return data


def broadcast(host, port=5000, message):
	data = getdata(message)
	length = len(data)

	sckt = socket.socket(AF_INET, SOCK_DGRAM)
	sckt.bind(('', 0))
	sckt.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


	totalsent = 0
	while totalsent < length:
		sent = sckt.sendto(data[totalsent:], ('<broadcast>', port))
		if not sent:
			raise RuntimeError('Socket connection broken!')
		totalsent = totalsent + sent
