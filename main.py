import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import uvicorn
import asyncio
from threading import Thread
import argparse

# Data Models
@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Block:
    index: int
    transactions: List[Transaction]
    timestamp: float
    previous_hash: str
    nonce: int = 0
    hash: str = None
    
    def __post_init__(self):
        if self.hash is None:
            self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")
    
    def to_dict(self):
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 4
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 100
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self, mining_reward_address: str):
        reward_transaction = Transaction(None, mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)
        
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
    
    def get_balance(self, address: str):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        return balance
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def replace_chain(self, new_chain: List[Dict]):
        new_blockchain = []
        for block_data in new_chain:
            transactions = [Transaction(**tx) for tx in block_data['transactions']]
            block = Block(
                block_data['index'],
                transactions,
                block_data['timestamp'],
                block_data['previous_hash'],
                block_data['nonce'],
                block_data['hash']
            )
            new_blockchain.append(block)
        
        if len(new_blockchain) > len(self.chain) and self._is_valid_chain(new_blockchain):
            self.chain = new_blockchain
            return True
        return False
    
    def _is_valid_chain(self, chain: List[Block]):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def to_dict(self):
        return [block.to_dict() for block in self.chain]

# Pydantic Models for API
class TransactionModel(BaseModel):
    sender: str
    recipient: str
    amount: float

class NodeModel(BaseModel):
    address: str

# FastAPI App
app = FastAPI(title="P2P Blockchain Network")

# Global variables
blockchain = Blockchain()
peers = set()
node_identifier = None
node_port = None

# Templates
templates = Jinja2Templates(directory="templates")

# API Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "node_port": node_port,
        "node_identifier": node_identifier
    })

@app.get("/api/chain")
async def get_chain():
    return {
        "chain": blockchain.to_dict(),
        "length": len(blockchain.chain)
    }

@app.get("/api/nodes")
async def get_nodes():
    return {"nodes": list(peers)}

@app.post("/api/nodes/register")
async def register_node(node: NodeModel):
    peers.add(node.address)
    return {"message": f"Node {node.address} registered successfully"}

@app.post("/api/transactions/new")
async def new_transaction(transaction: TransactionModel):
    tx = Transaction(transaction.sender, transaction.recipient, transaction.amount)
    blockchain.add_transaction(tx)
    return {"message": "Transaction added to pending pool"}

@app.get("/api/transactions/pending")
async def get_pending_transactions():
    return {
        "transactions": [tx.to_dict() for tx in blockchain.pending_transactions]
    }

@app.post("/api/mine")
async def mine_block():
    if not blockchain.pending_transactions:
        return {"message": "No pending transactions to mine"}
    
    blockchain.mine_pending_transactions(node_identifier)
    return {
        "message": "Block mined successfully",
        "block": blockchain.get_latest_block().to_dict()
    }

@app.get("/api/balance/{address}")
async def get_balance(address: str):
    balance = blockchain.get_balance(address)
    return {"address": address, "balance": balance}

@app.post("/api/consensus")
async def consensus():
    replaced = False
    max_length = len(blockchain.chain)
    new_chain = None
    
    for peer in peers:
        try:
            response = requests.get(f"http://{peer}/api/chain", timeout=5)
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain = data['chain']
                
                if length > max_length:
                    max_length = length
                    new_chain = chain
        except:
            continue
    
    if new_chain:
        if blockchain.replace_chain(new_chain):
            replaced = True
    
    return {
        "message": "Chain replaced" if replaced else "Chain is authoritative",
        "chain": blockchain.to_dict()
    }

@app.get("/api/validate")
async def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return {"valid": is_valid}

@app.get("/api/stats")
async def get_stats():
    return {
        "total_blocks": len(blockchain.chain),
        "pending_transactions": len(blockchain.pending_transactions),
        "difficulty": blockchain.difficulty,
        "peers": len(peers),
        "is_valid": blockchain.is_chain_valid()
    }

def create_app_with_port(port: int):
    global node_port, node_identifier
    node_port = port
    node_identifier = f"node_{port}"
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run P2P Blockchain Node')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the node on')
    args = parser.parse_args()
    
    app = create_app_with_port(args.port)
    uvicorn.run(app, host="0.0.0.0", port=args.port)