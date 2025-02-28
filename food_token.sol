// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FoodToken {
    struct User {
        string name;
        string email;
        string phoneNumber;
        mapping(uint256 => TokenInfo) tokens;
        uint256[] tokenIds;
    }

    struct TokenInfo {
        bool exists;
        bool isRedeemed;
        uint256 creationTime;
        string ownerPhone;  // Added to track token owner
    }

    mapping(string => User) private usersByPhone;  // phoneNumber => User
    mapping(string => string) private emailToPhone;  // email => phoneNumber
    mapping(uint256 => TokenInfo) private tokenRegistry;  // tokenId => TokenInfo
    uint256 private tokenIdCounter;

    event UserRegistered(string phoneNumber, string name, string email);
    event TokenIssued(string phoneNumber, uint256 tokenId);
    event TokenRedeemed(uint256 tokenId);

    function userExists(string memory _phoneNumber) private view returns (bool) {
        return bytes(usersByPhone[_phoneNumber].name).length > 0;
    }

    function registerUser(
        string memory _name,
        string memory _email,
        string memory _phoneNumber
    ) public returns (bool) {
        require(!userExists(_phoneNumber), "Phone number already registered");
        require(bytes(_name).length > 0, "Name cannot be empty");
        require(bytes(_email).length > 0, "Email cannot be empty");
        require(bytes(_phoneNumber).length > 0, "Phone number cannot be empty");
        
        // Check if phone number already exists
        if (bytes(usersByPhone[_phoneNumber].phoneNumber).length > 0) {
            return false;
        }
        
        // Register new user
        User storage newUser = usersByPhone[_phoneNumber];
        newUser.name = _name;
        newUser.email = _email;
        newUser.phoneNumber = _phoneNumber;
        
        // Map email to phone number for lookup
        emailToPhone[_email] = _phoneNumber;
        
        emit UserRegistered(_phoneNumber, _name, _email);
        return true;
    }

    function issueToken(string memory _phoneNumber) public returns (uint256) {
        require(bytes(usersByPhone[_phoneNumber].phoneNumber).length > 0, "User not registered");
        
        uint256 newTokenId = tokenIdCounter++;
        
        // Store token in user's mapping
        usersByPhone[_phoneNumber].tokens[newTokenId] = TokenInfo({
            exists: true,
            isRedeemed: false,
            creationTime: block.timestamp,
            ownerPhone: _phoneNumber
        });
        usersByPhone[_phoneNumber].tokenIds.push(newTokenId);
        
        // Store token in global registry
        tokenRegistry[newTokenId] = TokenInfo({
            exists: true,
            isRedeemed: false,
            creationTime: block.timestamp,
            ownerPhone: _phoneNumber
        });
        
        emit TokenIssued(_phoneNumber, newTokenId);
        return newTokenId;
    }

    function redeemToken(uint256 _tokenId) public {
        require(tokenRegistry[_tokenId].exists, "Token does not exist");
        require(!tokenRegistry[_tokenId].isRedeemed, "Token already redeemed");
        
        tokenRegistry[_tokenId].isRedeemed = true;
        
        // Update token status in user's mapping as well
        string memory phoneNumber = tokenRegistry[_tokenId].ownerPhone;
        usersByPhone[phoneNumber].tokens[_tokenId].isRedeemed = true;
        
        emit TokenRedeemed(_tokenId);
    }

    function getUserInfo(
        string memory _phoneNumber,
        string memory _email
    ) public view returns (
        string memory name,
        string memory email,
        string memory phoneNumber,
        uint256[] memory tokenIds,
        bool exists
    ) {
        // Check if phone number matches stored email mapping
        if (keccak256(bytes(emailToPhone[_email])) != keccak256(bytes(_phoneNumber))) {
            return ("", "", "", new uint256[](0), false);
        }
        
        User storage user = usersByPhone[_phoneNumber];
        
        // Verify user exists
        if (bytes(user.phoneNumber).length == 0) {
            return ("", "", "", new uint256[](0), false);
        }
        
        return (
            user.name,
            user.email,
            user.phoneNumber,
            user.tokenIds,
            true
        );
    }

    function getTokenInfo(uint256 _tokenId) public view returns (
        bool exists,
        bool isRedeemed,
        uint256 creationTime,
        string memory ownerPhone
    ) {
        TokenInfo storage token = tokenRegistry[_tokenId];
        return (
            token.exists,
            token.isRedeemed,
            token.creationTime,
            token.ownerPhone
        );
    }
}