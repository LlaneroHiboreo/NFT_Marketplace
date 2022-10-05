import os
from brownie import Marketplace, accounts
import pytest
from web3 import Web3

def deploy_marketplace(fee, deployer):
    sc_mktpl = Marketplace.deploy(fee, {'from': deployer })
    return sc_mktpl

def main():
    deploy_marketplace(10, accounts[0])