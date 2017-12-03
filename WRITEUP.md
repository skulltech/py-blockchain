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
	def __init__(self, previous_header, records):
		self.previous_header = previous_header
		self.records = records
```

As we discussed, the block contains a list of records. But what are previous_header and nonce? The genius of blockchain lies in these only, and in the proof-of-work system.


### Basics of Proof-Of-Work

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

How would I go about hashing the block was a problem I had to face. I had to get a hash of the part of the block without the header, and store that in the header. This could be done in a few different ways - 

- Making a class which would contain a block minus the header, named something like `HeadlessBlock`. And then the `Block` class would contain an instance of `HeadlessBlock`, along with the hash of that instance.
- Making the hash of the data attributes of `Block` in that class itself.

Now, we could go about hashing in two different ways

- __Using the `hash` function.__
    The [`hash`](https://docs.python.org/3/library/functions.html#hash) function in Python is used for Hash Tables, like in dictionary. As you can see in [it's documentation](https://docs.python.org/3/library/functions.html#hash), it returns an integer 
    from an immutable type. It's not really suitable for general purpose cryptographically-secure hashing.
- __Using the module [`hashlib`](https://docs.python.org/3/library/hashlib.html).__
    This is a the library to use for getting secure hash of some data, using different hashing algorithms such as _SHA256_, _MD5_ etc. (MD5 is not really secure though). The hash funtions in hashlib accept _bytes-like object_ (one supporting the [buffer API](https://docs.python.org/3/c-api/buffer.html)) as input, so we have to get a bytes-like object from the block somehow. We're going to discuss how that can be done in a while.

Now we have to decide which approach are we going to use. It's not much of a dilemma though, the second approach easily wins, because of mainly two reasons - 
- The `hashlib` library is built for usage case such as ours, the `hash` function's usage case is specifically Hash Tables.
- We will have to broadcast a verified block over the network later, and for that we will have to obtain a byte-like object from the block object anyway, so going with the second approach will save us some headache in the future too. 

So, we decided we're gonna turn the block object into a sequence of bytes, or byte-like-object, but how? Well, it turns out this is a common tasks programmers have to do quite frequently. This process is called serialization, the Python-specific term for which is "Pickling". Here are some definitions of serializations which will hopefully make the concept of serilization crystal-clear for you.

From [Wikipedia](https://en.wikipedia.org/wiki/Serialization),  

> In computer science, in the context of data storage, serialization is the process of translating data structures or object state into a format that can be stored (for example, in a file or memory buffer) or transmitted (for example, across a network connection link) and reconstructed later (possibly in a different computer environment).

From the [official documentation of the Pickle module](https://docs.python.org/3/library/pickle.html) of Python,  

> “Pickling” is the process whereby a Python object hierarchy is converted into a byte stream, and “unpickling” is the inverse operation, whereby a byte stream (from a binary file or bytes-like object) is converted back into an object hierarchy.

Any object instance can be pickled and vice-versa using the following syntax,

```python
import pickle

pickl = pickle.dumps(obj)
obj = pickle.loads(pickl)
```

Here `pickl` is a `bytes` object, so it can be hashed using the functions from `hashlib`. Below is the code to do that - 

```python
import hashlib

digest = hashlib.sha256(pickl).hexdigest()
```

`digest` here is a string representing the hash as a hexstring.

So after implementing our somewhat-acceptable hashing technique to our already existing `Block`, we get the following code.

```python
import uuid
import pickle
import hashlib


def mine(headless):
	pickled = pickle.dumps(headless)
	
	header = hashlib.sha256(pickl).hexdigest() 
	while not valid(header):
		header = hashlib.sha256(pickl).hexdigest() 	
	return header


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
```

Here the HeadlessBlock class, as discussed before contains the header (i.e. hash) of the previous block, the records, and a nonce. The nonce gets initialized to a random value when it's created (using the uuid.uuid4() function). The value of the nonce can be changed (set to a random value) as many times as you want later, by calling the noncise function.

The verification of the headless block, or mining, happens in the mine function. Calling this function with a headless block passed to it as an argument will return a verified `Block`, whose header/hash satisfies the proof-of-work condition.


### Let the world know we did it!

Sending a verified block over the network (not sending, rather broadcasing, letting the world know!) is another problem we have to solve. for this we have a pretty powerful `sockets` library in Python. Let's dive into it!

Now, to be totally frank, I had little or no idea about sockets programming before this blockchain venture of mine, so I had to learn it from the scratch. So if you're in a similar position, I will let you know how I got my head around the concepts of sockets programming. Check this short article of mine where I discussed that.


##### The basic idea

The most brilliant aspect of Blockchain is it's 


## The Challenge

After reading the original paper by Satoshi Nakamoto (whoever may him be!), I got fascinated how simple but powerful the idea of Bitcoin/Blockchain is. The only other time I got feeling similar to this is when I watched [this video by Computerphile](https://www.youtube.com/watch?v=MijmeoH9LT4) on Unicode, Character encodings, and UTF-8. Anyway, leaving that aside, being amazed at the brilliant simplicity of the basic concept behind Blockchain, I took up a challenge myself, I would make a blockchain implementation, using just this paper as the blockchain-related resource. The implementation may turn out to be simple, but it has to be complete. And also, I would ofcourse allow myself to look-up about general programming stuffs, just not anything specifically about Blockchain or Bitcoin. 

Below in this write-up, I will document the way I did it. The writeup closely follows my actions and thought process in the order they originally appeared, but of course it doesn't follow it exactly, as that would confuse the hell out of anyone, including myself! This writeup can be interpreted as a tutorial or introduction to blockchain, or maybe a lesson in how a developer thinks when he writes a program, it's upto you!

