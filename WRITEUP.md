From the name itself, anyone can guess that Blockchain is, a chain of blocks! We have an intuitive idea of what a chain is, but what is this 'block'?

Here, a 'block' in a Blockchain contains a fixed number of records. A record can be anything, and in most cases it is a record of something happening in a point of time. The idea of a record can be made clearer by giving some examples. In the most usual usage case of blockchain, i.e crypto-currencies, records are transactions. Another example of record could be posts in a discussion board which uses Blockchain in the back-end.

Every block in a blockchain contains

- The hash of the previous block.
- A nonce.
- Some records (a predetermined number of them, that is)

Here is a basic implementation of a block.
