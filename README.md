# Food Token App

![Food_Token_Management](https://github.com/user-attachments/assets/1f79d704-260b-43db-ac16-60c1ed9056aa)


A decentralized application for managing food tokens using Ethereum smart contracts, with a FastAPI backend and Flask frontend.

## Prerequisites

- Node.js (v16 or higher)
- Python 3.8+
- Git
- npm or yarn
- pip (Python package manager)

## Project Setup

### 1. Clone the Repository

```bash
git clone -b master https://github.com/yourusername/food-token-app.git
cd food-token-app
```

### 2. Hardhat Setup and Configuration

1. Install Hardhat and dependencies:
```bash
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
```

2. Initialize Hardhat project:
```bash
npx hardhat init
```
Select "Create a JavaScript project" when prompted.

3. Start Hardhat node:
```bash
npx hardhat node
```
This will start a local Ethereum network and provide you with test accounts.

### 3. Smart Contract Deployment

Deploy food_token.sol using remix.ethereum.org

### 4. FastAPI Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install fastapi uvicorn web3 python-dotenv sqlalchemy
```

3. Create a `.env` file:
```env
CONTRACT_ADDRESS=your_deployed_contract_address
PROVIDER_URL=http://localhost:8545
ABI of smart contract in json
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### 5. Flask Frontend Setup

1. Install Flask dependencies:
```bash
pip install flask flask-wtf requests
```

2. Set up environment variables:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

3. Start the Flask server:
```bash
flask run --port 5000
```


## Security Considerations

1. Never commit private keys or sensitive data
2. Use environment variables for configuration
3. Implement proper input validation
4. Use secure CORS policies
5. Implement rate limiting
6. Add proper error handling

## Troubleshooting

Common issues and solutions:

1. **Hardhat Network Connection Issues**
   - Ensure Hardhat node is running
   - Check network configuration in hardhat.config.js

2. **Smart Contract Deployment Failures**
   - Verify account has sufficient ETH
   - Check contract compilation errors

3. **API Connection Issues**
   - Verify all services are running on correct ports
   - Check CORS configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Author

1. Dhruvkumar Patel

## License

MIT License
