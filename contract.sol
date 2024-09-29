// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeCapsule {
    struct Capsule {
        address creator;
        string message;
        uint unlockTime;
        bool revealed;
    }

    Capsule[] public capsules;

    event CapsuleCreated(uint index, address creator, uint unlockTime);
    event CapsuleRevealed(uint index, string message);

    function createCapsule(string memory _message, uint _unlockTime) public {
        require(_unlockTime > block.timestamp, "Unlock time must be in the future");
        capsules.push(Capsule(msg.sender, _message, _unlockTime, false));
        emit CapsuleCreated(capsules.length - 1, msg.sender, _unlockTime);
    }

    function revealCapsule(uint _index) public {
        require(_index < capsules.length, "Invalid capsule index");
        Capsule storage capsule = capsules[_index];
        require(capsule.creator == msg.sender, "You are not the creator of this capsule");
        require(block.timestamp >= capsule.unlockTime, "Capsule is still locked");
        require(!capsule.revealed, "Capsule already revealed");

        capsule.revealed = true;
        emit CapsuleRevealed(_index, capsule.message);
    }

    function getCapsuleCount() public view returns (uint) {
        return capsules.length;
    }

    function getCapsuleDetails(uint _index) public view returns (address, uint, bool) {
        require(_index < capsules.length, "Invalid capsule index");
        Capsule storage capsule = capsules[_index];
        return (capsule.creator, capsule.unlockTime, capsule.revealed);
    }

    function getCapsuleMessage(uint _index) public view returns (string memory) {
        require(_index < capsules.length, "Invalid capsule index");
        require(block.timestamp >= capsules[_index].unlockTime, "Capsule is still locked");
        require(capsules[_index].revealed, "Capsule not revealed yet");
        return capsules[_index].message;
    }
}
