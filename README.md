# Complete Setup Guide for P2P Blockchain Network

## Step-by-Step Installation in Visual Studio Code

### Prerequisites
- Python 3.8 or higher
- Visual Studio Code
- Git (optional)

### Step 1: Project Setup

1. **Open Visual Studio Code**

2. **Create a new folder for your project**:
   - Create a folder called `p2p-blockchain` on your desktop or preferred location
   - Open this folder in VS Code (File → Open Folder)

3. **Create the project structure**:
   In VS Code terminal (Terminal → New Terminal), create the following structure:
   ```bash
   mkdir templates
   ```

### Step 2: Create Project Files

Create the following files in your project folder:

#### 1. Create `main.py`
Copy the main FastAPI application code (the first artifact) into this file.

#### 2. Create `templates/dashboard.html`
- Create a file called `dashboard.html` inside the `templates` folder
- Copy the HTML template code (the second artifact) into this file

#### 3. Create `requirements.txt`
Copy the requirements content into this file.

#### 4. Create `README.md`
Copy the README content into this file.

#### 5. Create `run_network.py`
Copy the network runner script into this file.

### Step 3: Set Up Python Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv blockchain_env
   ```

2. **Activate the virtual environment**:
   - **Windows**: `blockchain_env\Scripts\activate`
   - **Mac/Linux**: `source blockchain_env/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Verify Installation

Your project structure should look like this:
```
p2p-blockchain/
├── main.py
├── templates/
│   └── dashboard.html
├── requirements.txt
├── README.md
├── run_network.py
└── blockchain_env/
```

### Step 5: Running the Network

#### Option A: Single Node Testing
```bash
python main.py --port 8000
```
Then open: http://localhost:8000

#### Option B: Full Network (Recommended)
```bash
python run_network.py
```
This will start 3 nodes on ports 8000, 8001, and 8002.

### Step 6: Testing the Network

1. **Open multiple browser tabs**:
   - Tab 1: http://localhost:8000
   - Tab 2: http://localhost:8001
   - Tab 3: http://localhost:8002

2. **Register peers on each node**:
   - Node 8000: Add `localhost:8001` and `localhost:8002`
   - Node 8001: Add `localhost:8000` and `localhost:8002`
   - Node 8002: Add `localhost:8000` and `localhost:8001`

3. **Create transactions**:
   - Use the transaction form to create transactions
   - Try different sender/recipient combinations

4. **Mine blocks**:
   - Click "Mine Block" on different nodes
   - Watch the mining progress

5. **Test consensus**:
   - Click "Sync Blockchain" to synchronize between nodes
   - Verify all nodes have the same blockchain

### Step 7: Common Operations

#### Creating Transactions
1. Fill in the transaction form:
   - Sender: `alice`
   - Recipient: `bob`
   - Amount: `10.0`
2. Click "Create Transaction"

#### Mining Blocks
1. Click "Mine Block" button
2. Wait for mining to complete
3. Check updated statistics

#### Checking Balances
1. Enter address (e.g., `alice`)
2. Click "Check Balance"

#### Syncing Network
1. Click "Sync Blockchain"
2. Verify consensus message

### Step 8: Advanced Testing Scenarios

#### Scenario 1: Network Partitioning
1. Start all nodes
2. Register peers
3. Create transactions on Node 1
4. Mine blocks on Node 1
5. Create different transactions on Node 2
6. Mine blocks on Node 2
7. Sync all nodes - longest chain wins

#### Scenario 2: Balance Verification
1. Create transaction: alice → bob (50 coins)
2. Mine block on any node
3. Check alice's balance (should decrease)
4. Check bob's balance (should increase)
5. Verify mining rewards

### Step 9: API Testing (Optional)

You can also test the API directly using curl or Postman:

```bash
# Get blockchain
curl http://localhost:8000/api/chain

# Create transaction
curl -X POST http://localhost:8000/api/transactions/new \
  -H "Content-Type: application/json" \
  -d '{"sender": "alice", "recipient": "bob", "amount": 10.0}'

# Mine block
curl -X POST http://localhost:8000/api/mine

# Check balance
curl http://localhost:8000/api/balance/alice

# Get stats
curl http://localhost:8000/api/stats
```

### Troubleshooting

#### Common Issues and Solutions

1. **Port already in use**:
   - Kill existing processes: `pkill -f "python main.py"`
   - Or use different ports: `python main.py --port 8003`

2. **Module not found**:
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

3. **Template not found**:
   - Check `templates/dashboard.html` exists
   - Verify folder structure

4. **Peers not connecting**:
   - Ensure all nodes are running
   - Check firewall settings
   - Use `localhost` instead of `127.0.0.1`

5. **Mining takes too long**:
   - Reduce difficulty in `main.py` (change `self.difficulty = 2`)

### Development Tips

1. **VS Code Extensions**:
   - Python extension
   - HTML CSS Support
   - REST Client (for API testing)

2. **Debugging**:
   - Use VS Code debugger
   - Add breakpoints in `main.py`
   - Check browser console for errors

3. **Customization**:
   - Modify UI colors in `dashboard.html`
   - Adjust mining difficulty
   - Add new API endpoints

### Assignment Deliverables Checklist

- ✅ **Source code with documentation**: All files created and documented
- ✅ **Blockchain implementation**: Complete with PoW mining
- ✅ **P2P network simulation**: Multiple nodes with peer discovery
- ✅ **Consensus algorithm**: Longest chain wins implementation
- ✅ **Node synchronization**: Peers can sync blockchains
- ✅ **Professional UI**: Modern web interface with all operations
- ✅ **README file**: Comprehensive documentation
- ✅ **Screenshots/logs**: Available through web interface
- ✅ **Bonus features**: HTML frontend, dashboard, transaction validation

### Performance Monitoring

Monitor your network with:
- Real-time statistics on dashboard
- Browser developer tools for network requests
- Terminal output for mining logs
- API endpoints for programmatic monitoring

### Next Steps

After completing the basic assignment, consider:
1. Adding digital signatures
2. Implementing transaction fees
3. Creating a mobile-responsive design
4. Adding WebSocket for real-time updates
5. Implementing different consensus algorithms
6. Adding data persistence

## Conclusion

This implementation provides a complete P2P blockchain network with professional UI and all required features. The modular design makes it easy to extend and customize for additional requirements.