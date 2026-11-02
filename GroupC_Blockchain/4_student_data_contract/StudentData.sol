// SPDX-License-Identifier: MIT
pragma solidity 0.8.38;

// C2: Student data using a structure, an array and the fallback function
contract StudentData {
    struct Student {
        uint256 rollNo;
        string name;
        uint256 marks;
    }

    Student[] students;                 // dynamic array of structures

    event Received(address sender, uint256 amount, string how);

    function addStudent(uint256 rollNo, string memory name, uint256 marks) public {
        students.push(Student(rollNo, name, marks));
    }

    function getStudent(uint256 index) public view returns (uint256, string memory, uint256) {
        Student memory s = students[index];   // reverts if index is out of range
        return (s.rollNo, s.name, s.marks);
    }

    function getCount() public view returns (uint256) {
        return students.length;
    }

    // runs when Ether is sent with no data
    receive() external payable {
        emit Received(msg.sender, msg.value, "receive");
    }

    // runs when a call matches no function
    fallback() external payable {
        emit Received(msg.sender, msg.value, "fallback");
    }
}
