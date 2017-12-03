import uuid
import pickle
import hashlib


def mine(headless):
	pickled = pickle.dumps(headless)
	header = hashlib.sha256(pickl).hexdigest()

	if valid(header):
		return Block(header, pickled)


class Block:
	def __init__(self, header, pickled):
		self.headless = pickled
		self.header = header


class HeadlessBlock:
	def __init__(self, previous_header, records):
		self.previous_header = previous_header
		self.records = records
		self.nonce = uuid.uuid4()

	def noncise(self):
		self.nonce = uuid.uuid4()


def valid(header):
	return (header % 2) != 0
