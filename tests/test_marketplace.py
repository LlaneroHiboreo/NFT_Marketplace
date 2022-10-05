import os
from brownie import accounts
from scripts.deploy_marketplace import deploy_marketplace
from scripts.deploy_nft import deploy_nft
import pytest
from web3 import Web3

# deploy contract tokens
@pytest.fixture
def test_setup_marketplace_and_nft():
    
    # set owner
    dply_acc0 = accounts[0]

    # deploy marketplace and nft contract
    dply_nft = deploy_nft('Nft_token', 'nftk', dply_acc0)
    dply_mktpl = deploy_marketplace(10, dply_acc0)

    return (dply_nft, dply_mktpl)

def test_mint_approvals_make(test_setup_marketplace_and_nft):
    # set users
    dply_acc0 = accounts[0] # deployer of smarct contracts
    usr_acc1 = accounts[1] # minter and seller
    usr_acc2 = accounts[2] # buyer

    # fetch contracts
    dply_nft = test_setup_marketplace_and_nft[0]
    dply_mktpl = test_setup_marketplace_and_nft[1]

    #TEST MINT
    # usr1 mints nft
    tx_transaction = dply_nft.mint("https://llanerohiboreo.github.io/Portfolio_Site/", {'from':usr_acc1})
    tx_transaction.wait(1)

    # check owner of nft is user 1
    assert dply_nft.ownerOf(1, {'from':dply_acc0}) == usr_acc1

    # APPROVAL marketplace
    tx_transaction = dply_nft.setApprovalForAll(dply_mktpl.address, True, {'from':usr_acc1})
    tx_transaction.wait(1)

    # MAKE ITEM
    price_item = Web3.toWei('10', 'Ether')
    tx_transaction = dply_mktpl.makeItem(dply_nft.address, 1, price_item, {'from':usr_acc1})
    tx_transaction.wait(1)

    # assert price
    assert dply_mktpl.Items(1)[3] == price_item
    # assert status sold/bought
    assert dply_mktpl.Items(1)[5] == False

    # BUY ITEM (price item + fees!!!)
    pay_item = Web3.toWei('12', 'Ether')
    tx_transaction = dply_mktpl.purchaseItem(1, {'from':usr_acc2, 'amount':pay_item})
    tx_transaction.wait(1)

    # assert status sold(true)/sale(false)
    assert dply_mktpl.Items(1)[5] == True

    # check token URI
    print(dply_nft.tokenURI(1))