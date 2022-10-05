// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract Marketplace is ReentrancyGuard{
    // This address gathers payments of all users
    address payable public immutable feeAccount;

    // This defines fees
    uint public immutable feePercent;

    // id variable
    uint public itemCount;

    struct Item{
        uint itemId;
        IERC721 nft;
        uint tokenId;
        uint price;
        address payable seller;
        bool sold;
    }

    // relate item with identifier
    mapping(uint=>Item) public Items;


    // Event to emit
    event Offered(
        uint itemID,
        address indexed nft,
        uint tokenID,
        uint price,
        address indexed seller
    );

    event Bought(
        uint itemId,
        address indexed nft,
        uint tokenID,
        uint price,
        address indexed seller,
        address indexed buyer
    );

    constructor(uint _feePercent){
        feeAccount = payable(msg.sender);
        feePercent = _feePercent;
    }

    function makeItem(IERC721 _nft, uint _tokenId, uint _price) external nonReentrant{
        require(_price > 0);
        itemCount++;
        _nft.transferFrom(msg.sender, address(this), _tokenId);
        Items[itemCount] = Item(
            itemCount,
            _nft,
            _tokenId,
            _price,
            payable(msg.sender),
            false 
        );
        emit Offered(itemCount, address(_nft), _tokenId, _price, msg.sender);
    }

    // function to buy item nft
    function purchaseItem(uint _itemId) external payable nonReentrant{
        uint _totalPrice = getTotalPrice(_itemId);
        Item storage item = Items[_itemId];
        require(_itemId > 0 && _itemId <= itemCount);
        require(msg.value >= _totalPrice);
        require(!item.sold);
        // the receiver (seller) will recive the amount of the nft price (item.price)
        item.seller.transfer(item.price);
        feeAccount.transfer(_totalPrice - item.price);
        item.sold = true;
        item.nft.transferFrom(address(this), msg.sender, item.tokenId);
        emit Bought(_itemId, address(item.nft), item.tokenId, item.price, item.seller, msg.sender);
    }

    // function to check item nft price
    function getTotalPrice(uint _itemId) view public returns(uint) {
        return ((Items[_itemId].price*(100+feePercent))/100);
    }

    
}