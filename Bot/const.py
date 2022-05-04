OWNER = "0x9c792C6b87504856Cb9427F8E33c776b624b2fC9"
BOT_TOKEN = "5261432831:AAEzrT-2Ug8mFhfDSHIEKdAgzpEmVa_R8s0"
USDT_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"

# MAINNET
BSC = "https://bsc-dataseed.binance.org/"
CHAIN_ID = 56
CONTRACT_ADDRESS = "0x9E061b5D37d7025E21aa377702B703696Df99f90"

# TESTNET
# BSC = "https://data-seed-prebsc-1-s1.binance.org:8545/"
# CHAIN_ID = 97
# CONTRACT_ADDRESS = "0x364A1C7eE72d4813877a3Ac9BeF8bA965e889f90"

BSC_SCAN_URL = "https://bscscan.com/tx/"
PRIV_KEY = "63457de7f40cfba9f89c211b502e5efef1f48b2e7ae18803338c4bbc5ee4eb6b"
ADMINS = ['221514152']#, '99347107']
USER_FILE = 'TDB/user_file.json'
TICKET_FILE = 'TDB/ticket_file.json'
TX_FILE = 'TDB/tx_file.txt'
FAILED_FILE = 'TDB/failed_file.txt'
PENDING_USERS_FILE = 'TDB/pending_users_file.json'
WINNERS_FILE = 'TDB/winners_file.json'
ABI = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "usdtAddress",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": "false",
		"inputs": [
			{
				"indexed": "false",
				"internalType": "string",
				"name": "_username",
				"type": "string"
			},
			{
				"indexed": "false",
				"internalType": "uint256",
				"name": "_lotteryId",
				"type": "uint256"
			},
			{
				"indexed": "false",
				"internalType": "uint256[]",
				"name": "_tokens",
				"type": "uint256[]"
			}
		],
		"name": "TicketRegister",
		"type": "event"
	},
	{
		"anonymous": "false",
		"inputs": [
			{
				"indexed": "false",
				"internalType": "string",
				"name": "_username",
				"type": "string"
			},
			{
				"indexed": "false",
				"internalType": "address",
				"name": "_wallet",
				"type": "address"
			},
			{
				"indexed": "false",
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "TransferUSDT",
		"type": "event"
	},
	{
		"anonymous": "false",
		"inputs": [
			{
				"indexed": "false",
				"internalType": "string",
				"name": "_username",
				"type": "string"
			},
			{
				"indexed": "false",
				"internalType": "address",
				"name": "_wallet",
				"type": "address"
			},
			{
				"indexed": "false",
				"internalType": "string",
				"name": "_referer",
				"type": "string"
			}
		],
		"name": "UserRegister",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "amountFixed",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "findWinners",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllWinnings",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getLotteryTokens",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getNumOfTickets",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getNumOfUsers",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getNumOfWinners",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "getTokens",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getUSDTBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usrnm",
				"type": "string"
			}
		],
		"name": "giveFreePass",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usrnm",
				"type": "string"
			}
		],
		"name": "hasReferer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "lotteryID",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usrnm",
				"type": "string"
			}
		],
		"name": "numberOfReferredUsers",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usrnm",
				"type": "string"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns",
				"type": "uint256[]"
			}
		],
		"name": "registerFreepassUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usr",
				"type": "string"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns",
				"type": "uint256[]"
			}
		],
		"name": "registerTicket",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usr",
				"type": "string"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns1",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns2",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns3",
				"type": "uint256[]"
			}
		],
		"name": "registerTickets",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usr",
				"type": "string"
			},
			{
				"internalType": "address payable",
				"name": "wllt",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "rfrr",
				"type": "string"
			}
		],
		"name": "registerUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usr",
				"type": "string"
			},
			{
				"internalType": "address payable",
				"name": "wllt",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "rfrr",
				"type": "string"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns1",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns2",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns3",
				"type": "uint256[]"
			}
		],
		"name": "registerUserTickets",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usr",
				"type": "string"
			},
			{
				"internalType": "address payable",
				"name": "wllt",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "rfrr",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "usr_",
				"type": "string"
			},
			{
				"internalType": "address payable",
				"name": "wllt_",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "rfrr_",
				"type": "string"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns1",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns2",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256[]",
				"name": "tkns3",
				"type": "uint256[]"
			}
		],
		"name": "registerUserTicketsRef",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "addr",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "sendBNB",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "addr",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "sendUSDT",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256[]",
				"name": "tokens",
				"type": "uint256[]"
			}
		],
		"name": "setLotteryTokens",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256[]",
				"name": "amounts",
				"type": "uint256[]"
			}
		],
		"name": "setRefWinnerAmounts",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usrnm",
				"type": "string"
			},
			{
				"internalType": "address payable",
				"name": "wllt",
				"type": "address"
			}
		],
		"name": "setWallet",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256[]",
				"name": "amounts",
				"type": "uint256[]"
			}
		],
		"name": "setWinnerAmounts",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usrnm",
				"type": "string"
			}
		],
		"name": "takeFreePass",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tickets",
		"outputs": [
			{
				"internalType": "string",
				"name": "username",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "transferToWinners",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "usdt",
		"outputs": [
			{
				"internalType": "contract IERC20",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "usrnm",
				"type": "string"
			}
		],
		"name": "userExists",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "users",
		"outputs": [
			{
				"internalType": "string",
				"name": "username",
				"type": "string"
			},
			{
				"internalType": "address payable",
				"name": "wallet",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "referer",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "freePass",
				"type": "bool"
			},
			{
				"internalType": "uint256",
				"name": "winAmount",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "winnerAmounts",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "winnerRefAmounts",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	}
]