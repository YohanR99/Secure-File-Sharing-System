import hashlib
import json
import os
from datetime import datetime

BLOCKCHAIN_FILE = 'blockchain.json'


class Block:
    def __init__(self, index, data, previous_hash, timestamp=None):
        self.index = index
        self.timestamp = timestamp or str(datetime.utcnow())
        self.data = data  # metadata dict
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data, sort_keys=True)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def load_chain(self):
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, 'r') as f:
                self.chain = json.load(f)
        else:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Initializes blockchain with the first (genesis) block."""
        genesis = Block(0, {"message": "Genesis Block"}, "0")
        self.chain = [genesis.to_dict()]
        self.save_chain()

    def add_block(self, data):
        """Appends a new block with given data to the blockchain."""
        last_block = self.chain[-1]
        index = last_block["index"] + 1
        new_block = Block(index, data, last_block["hash"])
        self.chain.append(new_block.to_dict())
        self.save_chain()

    def save_chain(self):
        """Persists the blockchain to disk."""
        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def validate_chain(self):
        """
        Validates the blockchain by ensuring:
        1. Each block's hash is correct.
        2. Each block links correctly to the previous block.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Recreate block to verify hash
            recalculated_hash = Block(
                current["index"],
                current["data"],
                current["previous_hash"],
                current["timestamp"]
            ).hash

            if current["hash"] != recalculated_hash:
                print(f"❌ Tampered block at index {i}")
                return False

            if current["previous_hash"] != previous["hash"]:
                print(f"❌ Invalid hash chain at block {i}")
                return False

        return True
