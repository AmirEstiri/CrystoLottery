// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Lottery {

    struct User {
        string username;
        address payable wallet;
        string referer;
        bool freePass;
        uint winAmount;
    }

    struct Ticket {
        string username;
        uint[] tokens;
    }

    event UserRegister(string _username, address _wallet, string _referer);
    event TicketRegister(string _username, uint _lotteryId, uint[] _tokens);
    event TransferUSDT(string _username, address _wallet, uint _amount);

    // USDT token
    IERC20 public usdt;
    // Lottery data
    User[] public users;
    Ticket[] public tickets;
    uint public lotteryID;
    // Admin info
    address payable public owner;
    // Hyper-parameters
    uint[] private lotteryTokens;
    uint[] public winnerAmounts;
    uint[] public winnerRefAmounts;
    bool[] public amountFixed;
    // Helper lists
    uint[] private winnersCnt;
    uint[] private winnersRefCnt;

    constructor(address usdtAddress) {
        // creator of the smart contract
        owner = payable(msg.sender);
        // current number of lottery 
        lotteryID = 1;
        // the winner tokens
        lotteryTokens = [2, 8, 12, 23, 33, 48];
        // number of (direct) winners with different scores
        winnersCnt = [0, 0, 0, 0, 0, 0, 0];
        // number of (indirect/reference) winners with different scores
        winnersRefCnt = [0, 0, 0, 0, 0, 0, 0];
        // amount of money to be paid to winners with different scores
        winnerAmounts = [0, 0, 1000000000000000000, 2000000000000000000, 3000000000000000000, 4000000000000000000, 5000000000000000000];
        // amount of money to be paid to (reference) winners with different scores
        winnerRefAmounts = [0, 0, 1000000000000000000, 1000000000000000000, 1000000000000000000, 1000000000000000000, 1000000000000000000];
        // shows if the money should be paid for each score absolute or divided between winners
        amountFixed = [true, true, true, true, true, false, false];
        // USDT token
        usdt = IERC20(usdtAddress);
    }

    receive() payable external {}

    // check if username exists in players list
    function userExists(string memory usrnm) public view returns (bool) {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                return true;
            }
        }
        return false;
    }


    // how many people have been referred by a user
    function numberOfReferredUsers(string memory usrnm) public view returns (uint) {
        uint cnt = 0;
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].referer, usrnm)) {
                cnt += 1;
            }
        }
        return cnt;
    }

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

    // change wallet for user
    function setWallet(string memory usrnm, address payable wllt) public onlyOwner {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                users[i].wallet = wllt;
            }
        }
    }

    // check if token is in correct format (6 non-duplicate numbers from 1to 50)
    function checkTokens(uint[] memory tkns) private pure returns (bool) {
        if (tkns.length != 6) {
            return false;
        }
        for (uint i=0; i<6; i++) {
            if (tkns[i] < 1 || tkns[i] > 50) {
                return false;
            }
            for (uint j=0; j<6; j++) {
                if (i != j && tkns[i] == tkns[j]) {
                    return false;
                }
            }
        }
        return true;
    }

    // register user in lottery
    function registerUser(string memory usr, address payable wllt, string memory rfrr) public onlyOwner {
        users.push(User(usr, wllt, rfrr, false, 0));
    }

    // register ticket in lottery
    function registerTicket(string memory usr, uint[] memory tkns) public onlyOwner {
        tickets.push(Ticket(usr, tkns));
    }

    // register 3 tickets in lottery
    function registerTickets(string memory usr, uint[] memory tkns1, uint[] memory tkns2, uint[] memory tkns3) public onlyOwner {
        tickets.push(Ticket(usr, tkns1));
        tickets.push(Ticket(usr, tkns2));
        tickets.push(Ticket(usr, tkns3));
    }

    // register user, user's tickets and user's ref in lottery
    function registerUserTicketsRef(string memory usr, address payable wllt, string memory rfrr, string memory usr_, address payable wllt_, string memory rfrr_, uint[] memory tkns1, uint[] memory tkns2, uint[] memory tkns3) public onlyOwner {
        users.push(User(usr, wllt, rfrr, false, 0));
        tickets.push(Ticket(usr, tkns1));
        tickets.push(Ticket(usr, tkns2));
        tickets.push(Ticket(usr, tkns3));
        users.push(User(usr_, wllt_, rfrr_, false, 0));
    }

    // register user and user's tickets in lottery
    function registerUserTickets(string memory usr, address payable wllt, string memory rfrr, uint[] memory tkns1, uint[] memory tkns2, uint[] memory tkns3) public onlyOwner {
        users.push(User(usr, wllt, rfrr, false, 0));
        tickets.push(Ticket(usr, tkns1));
        tickets.push(Ticket(usr, tkns2));
        tickets.push(Ticket(usr, tkns3));
    }

    // check if string is empty
    function emptyString(string memory s) private pure returns(bool) {
        bytes memory sByte = bytes(s);
        return sByte.length == 0;
    }

    // check if user has freepass
    function hasFreePass(string memory usrnm) private view returns(bool) {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                return users[i].freePass;
            }
        }
        return false;
    }

    // register freepass user in lottery
    function registerFreepassUser(string memory usrnm, uint[] memory tkns) public onlyOwner {
        if (userExists(usrnm)) {
            if (hasFreePass(usrnm)) {
                // create a ticket for the user, if username exists in players list, password matches the username and tokens are in correct format
                tickets.push(Ticket(usrnm, tkns));
                takeFreePass(usrnm);
            } else {
                revert("this user does not have freepass");
            }
        } else {
            revert("username does not exist in lottery");
        }
    }

    // helper-func score tokens
    function scoreToken(uint[] memory tok1, uint[] memory tok2) private pure returns (uint) {
        uint score = 0;
        for (uint i=0; i<tok1.length; i++) {
            for (uint j=0; j<tok2.length; j++) {
                if (tok1[i] == tok2[j]) {
                    score++;
                }
            }
        }
        return score;
    }

    // check for equality of strings    
    function compareStrings(string memory a, string memory b) private pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }

    // check if user has a valid referer
    function hasReferer(string memory usrnm) view public returns(bool) {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                return userExists(users[i].referer);
            }
        }
        return false;
    }

    // give freepass to a user
    function giveFreePass(string memory usrnm) public onlyOwner {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                users[i].freePass = true;
            }
        }
    }

    // take away freepass from a user
    function takeFreePass(string memory usrnm) public onlyOwner {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                users[i].freePass = false;
            }
        }
    }

    // add money to player (to be paid later)
    function addWinAmount(string memory usrnm, uint amnt) private onlyOwner {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                users[i].winAmount += amnt;
            }
        }
    }

    // add reference money to player (to be paid later)
    function addWinAmountToReferer(string memory usrnm, uint amnt) private onlyOwner {
        for (uint i=0; i<users.length; i++) {
            if (compareStrings(users[i].username, usrnm)) {
                addWinAmount(users[i].referer, amnt);
            }
        }
    }

    // calculate win amount for every user
    function findWinners() public onlyOwner {
        for (uint i=0; i<users.length; i++) {
            users[i].winAmount = 0;
        }
        // Calculate number of winners for each score
        for (uint i=0; i<tickets.length; i++) {
            uint score = scoreToken(tickets[i].tokens, lotteryTokens);
            winnersCnt[score]++;
            if (hasReferer(tickets[i].username)) {
                winnersRefCnt[score]++;
            }
            // if (score == 1) {
            //     giveFreePass(tickets[i].username);
            // }
        }
        for (uint i=0; i<6; i++) {
            if (amountFixed[i]) {
                winnersCnt[i] = 1;
                winnersRefCnt[i] = 1;
            }
        }
        // Calculate money for each ticket and add the amount to the player
        for (uint i=0; i<tickets.length; i++) {
            uint score = scoreToken(tickets[i].tokens, lotteryTokens);
            addWinAmount(tickets[i].username, uint(winnerAmounts[score] / winnersCnt[score]));
            if (hasReferer(tickets[i].username)) {
                addWinAmountToReferer(tickets[i].username, uint(winnerRefAmounts[score] / winnersRefCnt[score]));
            }
        }
    }

    // get the total amount of money to be paid to all players
    function getAllWinnings() public onlyOwner view returns (uint) {
        uint winningsAmnt = 0;
        for (uint i=0; i<users.length; i++) {
            winningsAmnt += users[i].winAmount;
        }
        return winningsAmnt;
    }

    // get the total number of winners in lottery
    function getNumOfWinners() public onlyOwner view returns(uint) {
        uint numWinners = 0;
        for (uint i=0; i<users.length; i++) {
            if (users[i].winAmount > 0) {
                numWinners++;
            }
        }
        return numWinners;
    }

    // get the total number of users in lottery
    function getNumOfUsers() public view returns (uint) {
        return users.length;
    }

    // get the total number of tickets in lottery
    function getNumOfTickets() public view returns (uint) {
        return tickets.length;
    }

    // send money to every user at once
    function transferToWinners() public onlyOwner {
        for (uint i=0; i<users.length; i++) {
            // send money to winners
            if (users[i].winAmount > 0) {
                usdt.transfer(users[i].wallet, users[i].winAmount);
                emit TransferUSDT(users[i].username, users[i].wallet, users[i].winAmount);
            }
            // clear win amount for every user
            users[i].winAmount = 0;
        }
        // Start new lottery
        // clear tickets
        uint l = tickets.length;
        for (uint i=0; i<l; i++) {
            tickets.pop();
        }
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

    // get tokens for a ticket using index
    function getTokens(uint id) public view onlyOwner returns (uint[] memory) {
        return tickets[id].tokens;
    }

    // only owner of the contract
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
}