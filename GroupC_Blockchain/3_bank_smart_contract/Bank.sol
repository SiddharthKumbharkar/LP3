// SPDX-License-Identifier: MIT
pragma solidity 0.8.38;

// C1: Bank account - deposit money, withdraw money, show balance
contract Bank {
    mapping(address => uint256) balances;   // each customer's balance, in wei

    function deposit() public payable {
        require(msg.value > 0, "Deposit must be greater than 0");
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;

        // Use call instead of transfer, and check if it succeeded
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }

    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}