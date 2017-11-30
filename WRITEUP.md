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