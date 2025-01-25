// Initialize Web3
if (typeof window.ethereum !== 'undefined') {
  console.log('MetaMask is installed!');
} else {
  alert('MetaMask is not installed!');
}

const web3 = new Web3(window.ethereum);
const contractAddress = '0xAa4666F01989d4114cf88C9f32152346413bE8CF'; // Deployed contract address
const contractABI = [
  {
    "inputs": [
      {
        "internalType": "address payable",
        "name": "recipient",
        "type": "address"
      }
    ],
    "name": "sendReward",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
];

const contract = new web3.eth.Contract(contractABI, contractAddress);

// Connect to MetaMask
async function connectMetaMask() {
  try {
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    console.log('Connected:', accounts[0]);
    return accounts[0]; // Return the connected account address
  } catch (error) {
    console.error('User denied account access or error:', error);
    alert('Please allow MetaMask to connect.');
  }
}

// Send Reward Function
async function sendReward(walletAddress) {
  // Request MetaMask account access
  const senderAddress = await connectMetaMask();

  // Check if MetaMask is connected
  if (!senderAddress) {
    alert('Please connect your MetaMask wallet!');
    return;
  }

  // Define the reward amount (e.g., 0.1 ETH)
  const rewardAmount = web3.utils.toWei('0.1', 'ether');

  try {
    // Call the smart contract function to send the reward
    await contract.methods.sendReward(walletAddress).send({ 
      from: senderAddress,
      value: rewardAmount 
    });
    alert('Reward sent successfully!');
  } catch (error) {
    console.error(error);
    alert('An error occurred while sending the reward.');
  }
}

// Event Listener for Form Submission
document.getElementById('walletForm').addEventListener('submit', function (event) {
  event.preventDefault();
  const walletAddress = document.getElementById('walletAddress').value;
  if (web3.utils.isAddress(walletAddress)) {
    sendReward(walletAddress);
  } else {
    alert('Please enter a valid Ethereum address.');
  }
});
