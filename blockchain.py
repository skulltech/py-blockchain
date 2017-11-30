import uuid

		
def work_valid(header):
	return (header % 2) != 0


class Block:
	def __init__(self, prevhash, records):
		self.prevhash = prevhash
		self.records = records
		self.nonce = None
		self.header = None

	def mine(self):
		nonce = uuid.uuid4()
		header = hash((self.prevhash, self.records, nonce))
		if work_valid(header):
			self.nonce = nonce
			self.header = header
			return True
		return False
