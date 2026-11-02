// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// Assignment 3: Bank account smart contract - deposit, withdraw, show balance.
/// Deploy on a test network (e.g. Sepolia via Remix + MetaMask) and observe
/// the gas cost and transaction fee for each operation.
contract Bank {
    mapping(address => uint256) private balances;

    event Deposited(address indexed account, uint256 amount, uint256 newBalance);
    event Withdrawn(address indexed account, uint256 amount, uint256 newBalance);

    function deposit() external payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value, balances[msg.sender]);
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "Withdraw amount must be greater than zero");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");

        emit Withdrawn(msg.sender, amount, balances[msg.sender]);
    }

    function showBalance() external view returns (uint256) {
        return balances[msg.sender];
    }
}
