import os
from brownie import NFT, accounts
import pytest
from web3 import Web3

def deploy_nft(tk_name, tk_symbol, deployer):
    sc_nft = NFT.deploy(tk_name, tk_symbol, {'from': deployer })
    return sc_nft

def main():
    deploy_nft("Token", "TK", accounts[0])