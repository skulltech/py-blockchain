import socket
import zlib


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def receive(host=get_ip(), port):
	print('[*] Listening for connections on: {host}:{port}'.format(host=host, port=port))
	
	conn = socket.socket(AF_INET, SOCK_DGRAM)
	conn.bind((host, port))

	data, addr = conn.recvfrom(16)
	print('[*] Connection from : {addr[0]}:{addr[1]}'.format(addr=addr))

	chunks = []
	bytes_received = 0
	length = int(data.decode('UTF-8'))

	checksum = int(conn.recv(10).decode('UTF-8'))
	
	while bytes_received < length:
		chunk = conn.recv(min(length-bytes_received, 1024))
		if not chunk:
			raise RuntimeError('Socket connection broken!')
		chunks.append(chunk)
		bytes_received = bytes_received + len(chunk)

	data = b''.join(chunks)
	if (zlib.crc32(data) != checksum):
		raise RuntimeError("Checksums don't match!")
	return data
