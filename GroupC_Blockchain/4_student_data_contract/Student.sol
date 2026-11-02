// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// Assignment 4: Student data stored on-chain using structs and arrays.
/// Deploy on Ethereum (test network) and observe the transaction fee and
/// gas values for adding/updating students vs. reading them back.
contract Student {
    struct StudentRecord {
        uint256 id;
        string name;
        uint256 age;
        uint256 marks;
    }

    StudentRecord[] private students;

    event StudentAdded(uint256 indexed id, string name);

    function addStudent(string calldata name, uint256 age, uint256 marks) external {
        uint256 newId = students.length;
        students.push(StudentRecord(newId, name, age, marks));
        emit StudentAdded(newId, name);
    }

    function getStudent(uint256 id) external view returns (StudentRecord memory) {
        require(id < students.length, "Student does not exist");
        return students[id];
    }

    function getAllStudents() external view returns (StudentRecord[] memory) {
        return students;
    }

    function totalStudents() external view returns (uint256) {
        return students.length;
    }
}
