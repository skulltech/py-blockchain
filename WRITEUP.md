Blockchain is a favorite buzzword among tech news-sites now-a-days. It seems like everybody is trying to use the word just to sound smart, even if they have have no idea how it works. I got interested in it too naturally, especially with the ever-continuous rise of price of Bitcoin and Ethereum, also startups starting to make clever things using Blockchain, it demands some attention from tech guys like me. So I decided to give it a shot.

The first thing I did was read the paper on Bitcoin by Satoshi Nakamoto, and that itself made me understand the genius of this technology. In a very simple and clever way, blockchain solves the double-spending problem of Internet currencies, eliminating any need for third-parties like banks or mints. I may be getting ahead now, so without diving headfirst into this, let me first clear up a few things.


## Writing a Blockchain using Python

From the name itself, we can guess that Blockchain is, a chain of 'Blocks'. In the case of cryptocurrencies like Bitcoin, these 'blocks' consist mainly of transactions, but the way I understand, the blocks can contain all kinds of 'records', records that need to be preserved and later queried. The use of the term 'records' makes us think of databases, and that thought-process is not so wrong. Blockchain can be thought of as a new way to look at database, a decentralized database without the need of a server. This also solves another problem, the problem of having a single point-of-failure. 


### Implementing 'Blocks'

From the name itself, anyone can guess that Blockchain is, a chain of blocks! We have an intuitive idea of what a chain is, but what is this 'block'?

Here, a 'block' in a Blockchain contains a fixed number of records. A record can be anything, and in most cases it is a record of something happening in a point of time. The idea of a record can be made clearer by giving some examples. In the most usual usage case of blockchain, i.e crypto-currencies, records are transactions. Another example of record could be posts in a discussion board which uses Blockchain in the back-end.

Every block in a blockchain contains

- The hash of the previous block.
- A nonce.
- Some records (a predetermined number of them, that is)

Here is a basic implementation of a block.

```python
class Block:
	def __init__(self, prevhash, records):
		self.prevhash = prevhash
		self.records = records
```

As we discussed, the block contains a list of records. But what is prevhash? The genius of blockchain lies in it only, and in the proof-of-work system.


### Proof-Of-Work

Before adding a block to the chain, the block must be verified through a proof-of-work process. This proof-of-work involves finding a nonce for which the hash of the block satisfies a predetermined condition. In the case of Bitcoin, this condition is having a predetermined number of zeroes at the start of the hash bitstring. As the outcome of the hash is unpredectible from the data of the hash, it will take a large number of trials to get a nonce that satisfies the proof-of-work condition.

```python
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
```


In the `mine(self)` function of the `Block` class, I am using `uuid.uuid4()` function of Python to generate a random identifier, which is then used as the nonce. Then a hash of the block (complete with the nonce) is being generated using `hash()`. Now this generated hash (also called header of the block) needs to be verified. This verification is being done by the `work_valid(header)` function, which takes an header as input and returns True of False depending upon whether it was valid or not. 

In the case `work_valid(header)` is `True`, we set the block's header to that specific header and return `True`. Otherwise, it returns `False`.

So as per our implementation, we'll have to call the `mine()` function of a block repetatively until it returns `True`. When it does, we can add it to the block.


### Now something about Hashing. 

How would I go about hashing the block was a problem I had to face. I had to store the part of the block without the header, and store the hash in the header. This could be done in a few different ways - 

- Making a class which would contain everything except the header of a block, named something like `HeadlessBlock`. And then the `Block` class would contain an instance of `HeadlessBlock` and the hash of that instance.
- Making the hash of the data attributes of `Block` in that class itself.

Now, we could go about hashing in two different ways

- __Using the `hash` function.__
    The [`hash`](https://docs.python.org/3/library/functions.html#hash) function in Python is used for Hash Tables, like in dictionary. As you can see in [it's documentation](https://docs.python.org/3/library/functions.html#hash), it returns an integer 
    from an immutable type. It's not really suitable for general purpose cryptographically-secure hashing.
- __Using the module `hashlib`.__
    This is a the library to use for getting secure hash of some data, using different hashing algorithms such as _SHA256_, _MD5_ etc. (MD5 is not really secure though).

Now we have to decide which approach are we going to use. It's not much of a dilemma though, the second approach easily wins, because of mainly two reasons - 
- The `hashlib` library is for usage case such as ours, the `hash` function's usage case is specifically Hash Tables.
- We will have to broadcast a verified block over the network later, and for that we will have to obtain a byte-like object, or maybe a string from the block object anyway, so going with the second approach will save us some headache in the future too. 

The hash funtions in hashlib accept _bytes-like object_ (one supporting the [buffer API](https://docs.python.org/3/c-api/buffer.html) as input, so we have to get a bytes-like object from the block somehow.
