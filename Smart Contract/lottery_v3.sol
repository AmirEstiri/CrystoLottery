// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Lottery {

    event TransferUSDT(string _username, address _wallet, uint _amount);

    // USDT token
    IERC20 public usdt;
    // Lottery data
    uint public lotteryID;
    // Admin info
    address payable public owner;
    // Hyper-parameters
    uint[] private lotteryTokens;
    uint[] public winnerAmounts;
    uint[] public winnerRefAmounts;
    bool[] public amountFixed;

    constructor(address usdtAddress) {
        // creator of the smart contract
        owner = payable(msg.sender);
        // current number of lottery 
        lotteryID = 1;
        // the winner tokens
        lotteryTokens = [1, 2, 3, 4, 5, 6];
        // amount of money to be paid to winners with different scores
        winnerAmounts = [0, 0, 10, 20, 30, 40, 50];
        // amount of money to be paid to (reference) winners with different scores
        winnerRefAmounts = [0, 0, 10, 10, 10, 10, 10];
        // shows if the money should be paid for each score absolute or divided between winners
        amountFixed = [true, true, true, true, true, true, true];
        // USDT token
        usdt = IERC20(usdtAddress);
    }

    receive() payable external {}


    // get lottery tokens
    function getLotteryTokens() public onlyOwner view returns (uint[] memory) {
        return lotteryTokens;
    }

    // set lottery tokens
    function setLotteryTokens(uint[] memory tokens) public onlyOwner {
        lotteryTokens = tokens;
    }

    // set win amounts
    function setWinnerAmounts(uint[] memory amounts) public onlyOwner {
        winnerAmounts = amounts;
    }

    // set reference win amounts
    function setRefWinnerAmounts(uint[] memory amounts) public onlyOwner {
        winnerRefAmounts = amounts;
    }

    // send money to every user at once
    function NextLottery() public onlyOwner {
        lotteryID++;
    }

    // get lottery balance
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }

    // get usdt balance of lottery
    function getUSDTBalance() public view returns (uint) {
        return usdt.balanceOf(address(this));
    }

    // send USDT to wallet
    function sendUSDT(address payable addr, uint amount) public onlyOwner {
        usdt.transfer(addr, amount);
        emit TransferUSDT("UNKNOWN", addr, amount);
    }

    // send BNB to wallet
    function sendBNB(address payable addr, uint amount) public onlyOwner {
        addr.transfer(amount);
    }

    // only owner of the contract
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
}