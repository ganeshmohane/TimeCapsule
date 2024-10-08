from flask import Flask, render_template, jsonify, request
from web3 import Web3
import json
import time

app = Flask(__name__)

# Connect to the local Ethereum node (adjust as per your setup)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Contract ABI and Address (adjust according to deployment)
with open('contract_abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)
contract_address = Web3.to_checksum_address('0xa7442b1ae840e9cf61dcc547ccef0b8883bd9e21')
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Set default account for Flask app (or you can allow the user to input it)
default_account = web3.eth.accounts[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_capsule', methods=['POST'])
def create_capsule():
    data = request.json
    message = data['message']
    print(data,'data recieved')
    
    # Convert unlockTime from float to integer
    unlock_time = int(data['unlockTime'])  # Ensure unlockTime is sent as an integer (in seconds)
    print(unlock_time,'unlock time - user input')

    tx_hash = contract.functions.createCapsule(message, unlock_time).transact({
        'from': default_account
    })
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return jsonify({'status': 'Capsule created successfully', 'transactionHash': tx_hash.hex()})


from flask import jsonify
import time
from datetime import datetime

@app.route('/get_capsules')
def get_capsules():
    capsule_count = contract.functions.getCapsuleCount().call()
    capsules = []

    for i in range(capsule_count):
        creator, unlock_time, revealed = contract.functions.getCapsuleDetails(i).call()
        
        # Calculate remaining time in seconds
        current_time = int(time.time())
        remaining_time = max(0, unlock_time - current_time)
        
        # Convert UNIX time to a readable date format
        unlock_time_readable = datetime.fromtimestamp(unlock_time).strftime('%Y-%m-%d %H:%M:%S')
        print(unlock_time_readable)
        capsules.append({
            'index': i,
            'creator': creator,
            'remainingTime': remaining_time,
            'unlockTime': unlock_time_readable,  # Add the readable unlock time
            'revealed': revealed
        })
    
    return jsonify(capsules)


@app.route('/reveal_capsule', methods=['POST'])
def reveal_capsule():
    data = request.json
    capsule_index = data['index']

    tx_hash = contract.functions.revealCapsule(capsule_index).transact({
        'from': default_account
    })
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return jsonify({'status': 'Capsule revealed successfully', 'transactionHash': tx_hash.hex()})

@app.route('/get_capsule_message', methods=['POST'])
def get_capsule_message():
    data = request.json
    capsule_index = data['index']

    message = contract.functions.getCapsuleMessage(capsule_index).call()

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)
