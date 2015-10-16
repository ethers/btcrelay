from ethereum import tester
from datetime import datetime, date
from collections import namedtuple

import time

import pytest
slow = pytest.mark.slow

from utilRelay import makeMerkleProof, randomMerkleProof, \
    getHeaderBytes, dblSha256Flip, disablePyethLogging

disablePyethLogging()


# from contracts.json via Truffle
TOKEN_FACTORY_EVM = '60606040526110f6806100136000396000f30060606040526000357c01000000000000000000000000000000000000000000000000000000009004806305215b2f1461004f5780635f8dead31461008c578063dc3f65d3146100cf5761004d565b005b610060600480359060200150610231565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100a3600480359060200180359060200150610124565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100da600450610175565b60405180806020018281038252838181518152602001915080519060200190602002808383829060006004602084601f0104600302600f01f1509050019250505060405180910390f35b60006000506020528160005260406000206000508181548110156100025790600052602060002090016000915091509054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6020604051908101604052806000815260200150600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005080548060200260200160405190810160405280929190818152602001828054801561022257602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16815260200190600101908083116101ee575b5050505050905061022e565b90565b600060006000600084604051610c8d8061046983390180828152602001915050604051809103906000f092508291508173ffffffffffffffffffffffffffffffffffffffff1663c86a90fe8633604051837c0100000000000000000000000000000000000000000000000000000000028152600401808381526020018273ffffffffffffffffffffffffffffffffffffffff168152602001925050506020604051808303816000876161da5a03f1156100025750505060405151506001600060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000508181540191508181548183558181151161036957818360005260206000209182019101610368919061034a565b80821115610364576000818150600090555060010161034a565b5090565b5b505050905082600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060018303815481101561000257906000526020600020900160006101000a81548173ffffffffffffffffffffffffffffffffffffffff0219169083021790555080600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081815481835581811511610454578183600052602060002091820191016104539190610435565b8082111561044f5760008181506000905550600101610435565b5090565b5b50505050829350610460565b50505091905056006060604052604051602080610c8d8339016040526060805190602001505b80600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b50610c2b806100626000396000f300606060405236156100b6576000357c0100000000000000000000000000000000000000000000000000000000900480631fa03a2b146100b857806321af4feb146100e557806327e235e314610112578063673448dd1461013957806367eae67214610160578063930b7a2314610193578063bbd39ac0146101ac578063c86a90fe146101d3578063d26c8a8a14610200578063daea85c514610221578063f4b1604514610234578063fbf1f78a14610261576100b6565b005b6100cf600480359060200180359060200150610ace565b6040518082815260200191505060405180910390f35b6100fc600480359060200180359060200150610c00565b6040518082815260200191505060405180910390f35b610123600480359060200150610bb0565b6040518082815260200191505060405180910390f35b61014a6004803590602001506109ed565b6040518082815260200191505060405180910390f35b61017d6004803590602001803590602001803590602001506103a8565b6040518082815260200191505060405180910390f35b6101aa600480359060200180359060200150610789565b005b6101bd600480359060200150610674565b6040518082815260200191505060405180910390f35b6101ea600480359060200180359060200150610274565b6040518082815260200191505060405180910390f35b61020b600450610638565b6040518082815260200191505060405180910390f35b6102326004803590602001506106b2565b005b61024b600480359060200180359060200150610bcb565b6040518082815260200191505060405180910390f35b610272600480359060200150610851565b005b600082600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156103985782600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555082600060005060008473ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146856040518082815260200191505060405180910390a3600190506103a2566103a1565b600090506103a2565b5b92915050565b6000600083600060005060008773ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156106265760009050600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161561045c57600190508050610525565b600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505484111515610524576001905080506000600260005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b5b60018114156106185783600060005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555083600060005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168573ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146866040518082815260200191505060405180910390a36001915061063056610621565b60009150610630565b61062f565b60009150610630565b5b509392505050565b6000600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050549050610671565b90565b6000600060005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506106ad565b919050565b6001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060016040518082815260200191505060405180910390a35b50565b80600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e836040518082815260200191505060405180910390a35b5050565b6000600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060006040518082815260200191505060405180910390a38073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e60006040518082815260200191505060405180910390a35b50565b60006001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610aba57506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610ac85760019050610ac9565b5b919050565b60006001600160005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610b9b57506000600260005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610ba95760019050610baa565b5b92915050565b60006000506020528060005260406000206000915090505481565b60016000506020528160005260406000206000506020528060005260406000206000915091509054906101000a900460ff1681565b600260005060205281600052604060002060005060205280600052604060002060009150915050548156'
TOKEN_FACTORY_ABI = '[{"inputs":[{"type":"uint256","name":"_initialAmount"}],"constant":false,"name":"createStandardToken","outputs":[{"type":"address","name":""}],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"uint256","name":""}],"constant":true,"name":"created","outputs":[{"type":"address","name":""}],"type":"function"},{"inputs":[],"constant":false,"name":"createdByMe","outputs":[{"type":"address[]","name":""}],"type":"function"}]';

TOKEN_CONTRACT_ABI = '[{"inputs":[{"type":"address","name":"_target"},{"type":"address","name":"_proxy"}],"constant":true,"name":"isApprovedFor","outputs":[{"type":"bool","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"address","name":""}],"constant":true,"name":"approved_once","outputs":[{"type":"uint256","name":""}],"type":"function"},{"inputs":[{"type":"address","name":""}],"constant":true,"name":"balances","outputs":[{"type":"uint256","name":""}],"type":"function"},{"inputs":[{"type":"address","name":"_proxy"}],"constant":true,"name":"isApproved","outputs":[{"type":"bool","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_from"},{"type":"uint256","name":"_value"},{"type":"address","name":"_to"}],"constant":false,"name":"sendCoinFrom","outputs":[{"type":"bool","name":"_success"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":true,"name":"who","outputs":[{"type":"address","name":"_r"}],"type":"function"},{"inputs":[],"constant":true,"name":"sendr","outputs":[{"type":"address","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"},{"type":"uint256","name":"_maxValue"}],"constant":false,"name":"approveOnce","outputs":[],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":true,"name":"coinBalanceOf","outputs":[{"type":"uint256","name":"_r"}],"type":"function"},{"inputs":[{"type":"uint256","name":"_value"},{"type":"address","name":"_to"}],"constant":false,"name":"sendCoin","outputs":[{"type":"bool","name":"_success"}],"type":"function"},{"inputs":[],"constant":true,"name":"coinBalance","outputs":[{"type":"uint256","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":false,"name":"approve","outputs":[],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"address","name":""}],"constant":true,"name":"approved","outputs":[{"type":"bool","name":""}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":false,"name":"unapprove","outputs":[],"type":"function"},{"inputs":[{"type":"uint256","name":"_initialAmount"}],"type":"constructor"},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"uint256","name":"value"}],"type":"event","name":"CoinTransfer","anonymous":false},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"bool","name":"result"}],"type":"event","name":"AddressApproval","anonymous":false},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"uint256","name":"value"}],"type":"event","name":"AddressApprovalOnce","anonymous":false}]'

TOKEN_ENDOWMENT = 2**200
REWARD_PER_HEADER = 1000
INIT_FEE_VERIFY_TX = 10000000000000000  # 0.01 ETH
TOTAL_FEE_RELAY_TX = 0 + INIT_FEE_VERIFY_TX
MAX_DELTA_INCREASE_FVTX = int(INIT_FEE_VERIFY_TX*127/127.0/1024.0)  # FVTX FEE_VERIFY_TX
MAX_DELTA_DECREASE_FVTX = int(INIT_FEE_VERIFY_TX*-128/127.0/1024.0)

Account = namedtuple('Account', ['key', 'addr'])


class TestTokens(object):

    CONTRACT = 'btcBulkStoreHeaders.se'
    BTC_ETH_CONTRACT = 'test/btc-eth_debug.se'

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(2.9e6)
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT)

        initBtcRelayTokens(cls, tester)

        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    # based on test_btcBulkStoreHeaders testTx1In300K
    def testChargeOneRelayTx(self):
        numHeader = 12
        keySender = tester.k0
        addrSender = tester.a0
        hh = self.bulkStoreFrom300K(numHeader, keySender, addrSender)

        txIndex = 1
        # block300k tx[1] 7301b595279ece985f0c415e420e425451fcf7f684fcce087ba14d10ffec1121
        txStr = '01000000014dff4050dcee16672e48d755c6dd25d324492b5ea306f85a3ab23b4df26e16e9000000008c493046022100cb6dc911ef0bae0ab0e6265a45f25e081fc7ea4975517c9f848f82bc2b80a909022100e30fb6bb4fb64f414c351ed3abaed7491b8f0b1b9bcd75286036df8bfabc3ea5014104b70574006425b61867d2cbb8de7c26095fbc00ba4041b061cf75b85699cb2b449c6758741f640adffa356406632610efb267cb1efa0442c207059dd7fd652eeaffffffff020049d971020000001976a91461cf5af7bb84348df3fd695672e53c7d5b3f3db988ac30601c0c060000001976a914fd4ed114ef85d350d6d40ed3f6dc23743f8f99c488ac00000000'
        btcAddr = 0x61cf5af7bb84348df3fd695672e53c7d5b3f3db9
        self.checkRelay(txStr, txIndex, btcAddr, hh, numHeader, keySender, addrSender)


    # based on test_txVerify test30BlockValidTx
    def testChargeOneVerifyTx(self):
        numHeader = 24  # minimum is 24 (block 300017 plus 6 confirmations)
        keySender = tester.k0
        addrSender = tester.a0
        self.storeHeadersFrom300K(numHeader, keySender, addrSender)

        # block 300017
        header = {'nonce': 2022856018, 'hash': u'000000000000000032c0ae55f7f52b179a6346bb0d981af55394a3b9cdc556ea', 'timestamp': 1399708353, 'merkle_root': u'2fcb4296ba8d2cc5748a9310bac31d2652389c4d70014ccf742d0e4409a612c9', 'version': 2, 'prevhash': u'00000000000000002ec86a542e2cefe62dcec8ac2317a1dc92fbb094f9d30941', 'bits': 419465580}
        hashes = [u'29d2afa00c4947965717542a9fcf31aa0d0f81cbe590c9b794b8c55d7a4803de', u'84d4e48925445ef3b5722edaad229447f6ef7c77dfdb3b67b288a2e9dac97ebf', u'9f1ddd2fed16b0615d8cdd99456f5229ff004ea93234256571972d8c4eda05dd', u'ca31ee6fecd2d054b85449fb52d2b2bd9f8777b5e603a02d7de53c09e300d127', u'521eabbe29ce215b4b309db7807ed8f655ddb34233b2cfe8178522a335154923', u'a03159699523335896ec6d1ce0a18b247a3373b288cefe6ed5d14ddeeb71db45', u'810a3a390a4b565a54606dd0921985047cf940070b0c61a82225fc742aa4a2e3', u'161400e37071b7096ca6746e9aa388e256d2fe8816cec49cdd73de82f9dae15d', u'af355fbfcf63b67a219de308227dca5c2905c47331a8233613e7f7ac4bacc875', u'1c433a2359318372a859c94ace4cd2b1d5f565ae2c8496ef8255e098c710b9d4', u'49e09d2f48a8f11e13864f7daca8c6b1189507511a743149e16e16bca1858f80', u'5fd034ffd19cda72a78f7bacfd7d9b7b0bc64bc2d3135382db29238aa4d3dd03', u'74ab68a617c8419e6cbae05019a2c81fea6439e233550e5257d9411677845f34', u'df2650bdfcb4efe5726269148828ac18e2a1990c15f7d01d572252656421e896', u'1501aa1dbcada110009fe09e9cec5820fce07e4178af45869358651db4e2b282', u'41f96bb7e58018722c4d0dae2f6f4381bb1d461d3a61eac8b77ffe274b535292', u'aaf9b4e66d5dadb4b4f1107750a18e705ce4b4683e161eb3b1eaa04734218356', u'56639831c523b68cac6848f51d2b39e062ab5ff0b6f2a7dea33765f8e049b0b2', u'3a86f1f34e5d4f8cded3f8b22d6fe4b5741247be7ed164ca140bdb18c9ea7f45', u'da0322e4b634ec8dac5f9b173a2fe7f6e18e5220a27834625a0cfe6d0680c6e8', u'f5d94d46d68a6e953356499eb5d962e2a65193cce160af40200ab1c43228752e', u'e725d4efd42d1213824c698ef4172cdbab683fe9c9170cc6ca552f52244806f6', u'e7711581f7f9028f8f8b915fa0ddb091baade88036bf6f309e2d802043c3231d']
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, 1)


        eventArr = []
        self.s.block.log_listeners.append(lambda x: eventArr.append(self.c._translator.listen(x)))


        ethBal = self.s.block.get_balance(addrSender)
        res = self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=keySender, value=INIT_FEE_VERIFY_TX, profiling=True)
        print('GAS: '+str(res['gas']))
        assert res['output'] == 1  # adjust according to numHeader and the block that the tx belongs to

        assert self.s.block.get_balance(addrSender) == ethBal - INIT_FEE_VERIFY_TX
        assert self.s.block.get_balance(self.c.address) == INIT_FEE_VERIFY_TX


        assert eventArr == [{'_event_type': 'ethPayment'}]
        eventArr.pop()


    def testNoPayVerifyTx(self):
        numHeader = 24  # minimum is 24 (block 300017 plus 6 confirmations)
        keySender = tester.k0
        addrSender = tester.a0
        self.storeHeadersFrom300K(numHeader, keySender, addrSender)

        # block 300017
        header = {'nonce': 2022856018, 'hash': u'000000000000000032c0ae55f7f52b179a6346bb0d981af55394a3b9cdc556ea', 'timestamp': 1399708353, 'merkle_root': u'2fcb4296ba8d2cc5748a9310bac31d2652389c4d70014ccf742d0e4409a612c9', 'version': 2, 'prevhash': u'00000000000000002ec86a542e2cefe62dcec8ac2317a1dc92fbb094f9d30941', 'bits': 419465580}
        hashes = [u'29d2afa00c4947965717542a9fcf31aa0d0f81cbe590c9b794b8c55d7a4803de', u'84d4e48925445ef3b5722edaad229447f6ef7c77dfdb3b67b288a2e9dac97ebf', u'9f1ddd2fed16b0615d8cdd99456f5229ff004ea93234256571972d8c4eda05dd', u'ca31ee6fecd2d054b85449fb52d2b2bd9f8777b5e603a02d7de53c09e300d127', u'521eabbe29ce215b4b309db7807ed8f655ddb34233b2cfe8178522a335154923', u'a03159699523335896ec6d1ce0a18b247a3373b288cefe6ed5d14ddeeb71db45', u'810a3a390a4b565a54606dd0921985047cf940070b0c61a82225fc742aa4a2e3', u'161400e37071b7096ca6746e9aa388e256d2fe8816cec49cdd73de82f9dae15d', u'af355fbfcf63b67a219de308227dca5c2905c47331a8233613e7f7ac4bacc875', u'1c433a2359318372a859c94ace4cd2b1d5f565ae2c8496ef8255e098c710b9d4', u'49e09d2f48a8f11e13864f7daca8c6b1189507511a743149e16e16bca1858f80', u'5fd034ffd19cda72a78f7bacfd7d9b7b0bc64bc2d3135382db29238aa4d3dd03', u'74ab68a617c8419e6cbae05019a2c81fea6439e233550e5257d9411677845f34', u'df2650bdfcb4efe5726269148828ac18e2a1990c15f7d01d572252656421e896', u'1501aa1dbcada110009fe09e9cec5820fce07e4178af45869358651db4e2b282', u'41f96bb7e58018722c4d0dae2f6f4381bb1d461d3a61eac8b77ffe274b535292', u'aaf9b4e66d5dadb4b4f1107750a18e705ce4b4683e161eb3b1eaa04734218356', u'56639831c523b68cac6848f51d2b39e062ab5ff0b6f2a7dea33765f8e049b0b2', u'3a86f1f34e5d4f8cded3f8b22d6fe4b5741247be7ed164ca140bdb18c9ea7f45', u'da0322e4b634ec8dac5f9b173a2fe7f6e18e5220a27834625a0cfe6d0680c6e8', u'f5d94d46d68a6e953356499eb5d962e2a65193cce160af40200ab1c43228752e', u'e725d4efd42d1213824c698ef4172cdbab683fe9c9170cc6ca552f52244806f6', u'e7711581f7f9028f8f8b915fa0ddb091baade88036bf6f309e2d802043c3231d']
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, 1)

        ethBal = self.s.block.get_balance(addrSender)
        assert 0 == self.c.verifyTx(txHash, txIndex, siblings, txBlockHash)  # zero ETH sent

        assert self.s.block.get_balance(addrSender) == ethBal
        assert self.s.block.get_balance(self.c.address) == 0


    def testInsufficientPayVerifyTx(self):
        numHeader = 24  # minimum is 24 (block 300017 plus 6 confirmations)
        # headers are stored by k1, but k0 is who makes the verifyTx call
        verifier = Account(tester.k0, tester.a0)
        submitter = Account(tester.k1, tester.a1)
        self.storeHeadersFrom300K(numHeader, submitter.key, submitter.addr)

        # block 300017
        header = {'nonce': 2022856018, 'hash': u'000000000000000032c0ae55f7f52b179a6346bb0d981af55394a3b9cdc556ea', 'timestamp': 1399708353, 'merkle_root': u'2fcb4296ba8d2cc5748a9310bac31d2652389c4d70014ccf742d0e4409a612c9', 'version': 2, 'prevhash': u'00000000000000002ec86a542e2cefe62dcec8ac2317a1dc92fbb094f9d30941', 'bits': 419465580}
        hashes = [u'29d2afa00c4947965717542a9fcf31aa0d0f81cbe590c9b794b8c55d7a4803de', u'84d4e48925445ef3b5722edaad229447f6ef7c77dfdb3b67b288a2e9dac97ebf', u'9f1ddd2fed16b0615d8cdd99456f5229ff004ea93234256571972d8c4eda05dd', u'ca31ee6fecd2d054b85449fb52d2b2bd9f8777b5e603a02d7de53c09e300d127', u'521eabbe29ce215b4b309db7807ed8f655ddb34233b2cfe8178522a335154923', u'a03159699523335896ec6d1ce0a18b247a3373b288cefe6ed5d14ddeeb71db45', u'810a3a390a4b565a54606dd0921985047cf940070b0c61a82225fc742aa4a2e3', u'161400e37071b7096ca6746e9aa388e256d2fe8816cec49cdd73de82f9dae15d', u'af355fbfcf63b67a219de308227dca5c2905c47331a8233613e7f7ac4bacc875', u'1c433a2359318372a859c94ace4cd2b1d5f565ae2c8496ef8255e098c710b9d4', u'49e09d2f48a8f11e13864f7daca8c6b1189507511a743149e16e16bca1858f80', u'5fd034ffd19cda72a78f7bacfd7d9b7b0bc64bc2d3135382db29238aa4d3dd03', u'74ab68a617c8419e6cbae05019a2c81fea6439e233550e5257d9411677845f34', u'df2650bdfcb4efe5726269148828ac18e2a1990c15f7d01d572252656421e896', u'1501aa1dbcada110009fe09e9cec5820fce07e4178af45869358651db4e2b282', u'41f96bb7e58018722c4d0dae2f6f4381bb1d461d3a61eac8b77ffe274b535292', u'aaf9b4e66d5dadb4b4f1107750a18e705ce4b4683e161eb3b1eaa04734218356', u'56639831c523b68cac6848f51d2b39e062ab5ff0b6f2a7dea33765f8e049b0b2', u'3a86f1f34e5d4f8cded3f8b22d6fe4b5741247be7ed164ca140bdb18c9ea7f45', u'da0322e4b634ec8dac5f9b173a2fe7f6e18e5220a27834625a0cfe6d0680c6e8', u'f5d94d46d68a6e953356499eb5d962e2a65193cce160af40200ab1c43228752e', u'e725d4efd42d1213824c698ef4172cdbab683fe9c9170cc6ca552f52244806f6', u'e7711581f7f9028f8f8b915fa0ddb091baade88036bf6f309e2d802043c3231d']
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, 1)

        currFee = self.c.getFeeVerifyTx()

        expBalVerifier = self.s.block.get_balance(verifier.addr)
        expBalRelay = self.s.block.get_balance(self.c.address)

        valSend = currFee - 1
        expBalVerifier -= valSend
        expBalRelay += valSend
        assert 0 == self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=verifier.key, value=valSend)
        assert self.s.block.get_balance(verifier.addr) == expBalVerifier
        assert self.s.block.get_balance(self.c.address) == expBalRelay

        valSend = currFee
        expBalVerifier -= valSend
        expBalRelay += valSend
        assert 1 == self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=verifier.key, value=valSend)

        assert self.s.block.get_balance(verifier.addr) == expBalVerifier
        assert self.s.block.get_balance(self.c.address) == expBalRelay


    def testFeeVerifyTxMaxDecrease(self):
        newFee = self.checkAdjustFeeVerifyTx('00')
        assert newFee == INIT_FEE_VERIFY_TX + MAX_DELTA_DECREASE_FVTX
        self.s.revert(self.snapshot)
        assert self.checkAdjustFeeVerifyTx('') == newFee

    def testFeeVerifyTxMaxIncrease(self):
        feeUp = self.checkAdjustFeeVerifyTx('ff')
        assert feeUp == INIT_FEE_VERIFY_TX + MAX_DELTA_INCREASE_FVTX
        self.s.revert(self.snapshot)
        feeDown = self.checkAdjustFeeVerifyTx('01')
        assert (feeUp + feeDown) / 2 == INIT_FEE_VERIFY_TX  # deltas in feeUp and feeDown are equal

    def testFeeVerifyTxNoDecrease(self):
        newFee = self.checkAdjustFeeVerifyTx('80')
        assert newFee == INIT_FEE_VERIFY_TX

    def testFeeVerifyTxMinDecrease(self):
        newFee = self.checkAdjustFeeVerifyTx('7f')
        assert newFee == INIT_FEE_VERIFY_TX - 76894685039  # int(INIT_FEE_VERIFY_TX/127.0/1024.0)

    def testFeeVerifyTxMinIncrease(self):
        newFee = self.checkAdjustFeeVerifyTx('81')
        assert newFee == INIT_FEE_VERIFY_TX + 76894685039  # int(INIT_FEE_VERIFY_TX/127.0/1024.0)

    # based on testRewardOneBlock
    def checkAdjustFeeVerifyTx(self, feeFactor):
        block300K = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        self.c.setInitialParent(block300K, 299999, 1)
        blockHeaderStr = '0200000059c786bb379b65487f373279354f8ccc91ffcea2200c36080000000000000000dd9d7757a736fec629ab0ed0f602ba23c77afe7edec85a7026f641fd90bcf8f658ca8154747b1b1894fc742f'
        blockHeaderStr += feeFactor
        bhBytes = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBytes, profiling=True, sender=tester.k1)
        print('GAS: %s' % res['gas'])
        assert res['output'] == 300000

        # '0'+feeFactor trick per http://stackoverflow.com/a/31679342
        expFee = INIT_FEE_VERIFY_TX + self.deltaFee(int('0'+feeFactor, 16), INIT_FEE_VERIFY_TX)
        newFee = self.c.getFeeVerifyTx()
        assert newFee == expFee
        return newFee


    # feeFactor is in range [0, 255]
    # [0, 127] is decrease [129-255] is increase
    # thus max fee decrease is slightly more than max fee increase
    def deltaFee(self, feeFactor, currFee):
        return int(currFee * ((feeFactor - 128)/127.0) / 1024.0)


    # based on test_btcrelay testStoreBlockHeader
    def testRewardOneBlock(self):
        bal = self.xcoin.coinBalanceOf(self.c.address)
        assert bal == TOKEN_ENDOWMENT

        block300K = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        self.c.setInitialParent(block300K, 299999, 1)

        eventArr = []
        self.s.block.log_listeners.append(lambda x: eventArr.append(self.c._translator.listen(x)))


        blockHeaderStr = '0200000059c786bb379b65487f373279354f8ccc91ffcea2200c36080000000000000000dd9d7757a736fec629ab0ed0f602ba23c77afe7edec85a7026f641fd90bcf8f658ca8154747b1b1894fc742f'
        bhBytes = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBytes, profiling=True, sender=tester.k1)
        print('GAS: %s' % res['gas'])
        assert res['output'] == 300000

        # the first event is the CoinTransfer event from
        # Standard_Token: it probably should NOT be None but Serpent/pytester may
        # have issue with it and that's why it's None
        assert eventArr == [None, {'_event_type': 'rewardToken',
            'blockHeight': 300000,
            'rewardAddr': tester.a1.encode('hex')
            }]
        eventArr.pop()


        assert self.xcoin.coinBalanceOf(tester.a1) == REWARD_PER_HEADER

        bal = self.xcoin.coinBalanceOf(self.c.address)
        assert bal == TOKEN_ENDOWMENT - REWARD_PER_HEADER


    # based on test_btcrelay testHeadersFrom100K
    def testRewardOnlyMainChain(self):
        addrSender = tester.a0
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        # store only 2 headers for now
        for i in range(2):
            res = self.c.storeBlockHeader(blockHeaderBytes[i])
            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+100000

        expCoinsOfSender = 2*REWARD_PER_HEADER
        assert self.xcoin.coinBalanceOf(addrSender) == expCoinsOfSender

        # these are alternative blocks and store all 3,
        # but they do not have enough work and will not be on main chain
        # nonce: 0 blockhash: 11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        # nonce: 0 blockhash: 178930a916fa91dd29b2716387b7e024a6b3b2d2efa86bc45c86be223b07a4e5
        # nonce: 0 blockhash: 7b3c348edbb3645b34b30259105a941890e95e0ecc0a1c243ff48260d746e456
        EASIEST_DIFFICULTY_TARGET = 0x207fFFFFL
        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        time = 1293623863  # from block100k
        bits = EASIEST_DIFFICULTY_TARGET
        nonce = 1
        hashPrevBlock = block100kPrev
        for i in range(3):
            nonce = 1 if (i in [4,5]) else 0
            bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(bhBytes)
            hashPrevBlock = dblSha256Flip(bhBytes)

            assert res == i+100000  # fake blocks are stored since there is possibility they can become the main chain

        assert self.xcoin.coinBalanceOf(addrSender) == expCoinsOfSender

        # store a block with enough work that it extends the main chain
        assert 100002 == self.c.storeBlockHeader(blockHeaderBytes[2])
        assert self.xcoin.coinBalanceOf(addrSender) == expCoinsOfSender + REWARD_PER_HEADER


    # oneSender stores 2 headers; twoSender stores 1 header
    # Thus oneSender has 1/3 and 1/3 of tokens, and twoSender has 1/3.
    # These thirds are then cashed out in the following order:
    # twoSender cashes out, then oneSender cashes out half, then oneSender
    # cashes out remaining half. This effectively tests cashing out 1/3, 50%,
    # and then 100% of tokens.
    def testThirdsCashOut(self):
        Sender = namedtuple('Sender', ['key', 'addr', 'expCoins'])
        oneSender = Sender(tester.k1, tester.a1, 2*REWARD_PER_HEADER)

        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        # store only 2 headers for now
        for i in range(2):
            res = self.c.storeBlockHeader(blockHeaderBytes[i], sender=oneSender.key)
            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+100000

        assert self.xcoin.coinBalanceOf(oneSender.addr) == oneSender.expCoins

        twoSender = Sender(tester.k2, tester.a2, REWARD_PER_HEADER)
        assert 100002 == self.c.storeBlockHeader(blockHeaderBytes[2], sender=twoSender.key)
        assert self.xcoin.coinBalanceOf(twoSender.addr) == twoSender.expCoins


        keySender = tester.k0
        addrSender = tester.a0  # should be a0
        # block 300017
        header = {'nonce': 2022856018, 'hash': u'000000000000000032c0ae55f7f52b179a6346bb0d981af55394a3b9cdc556ea', 'timestamp': 1399708353, 'merkle_root': u'2fcb4296ba8d2cc5748a9310bac31d2652389c4d70014ccf742d0e4409a612c9', 'version': 2, 'prevhash': u'00000000000000002ec86a542e2cefe62dcec8ac2317a1dc92fbb094f9d30941', 'bits': 419465580}
        hashes = [u'29d2afa00c4947965717542a9fcf31aa0d0f81cbe590c9b794b8c55d7a4803de', u'84d4e48925445ef3b5722edaad229447f6ef7c77dfdb3b67b288a2e9dac97ebf', u'9f1ddd2fed16b0615d8cdd99456f5229ff004ea93234256571972d8c4eda05dd', u'ca31ee6fecd2d054b85449fb52d2b2bd9f8777b5e603a02d7de53c09e300d127', u'521eabbe29ce215b4b309db7807ed8f655ddb34233b2cfe8178522a335154923', u'a03159699523335896ec6d1ce0a18b247a3373b288cefe6ed5d14ddeeb71db45', u'810a3a390a4b565a54606dd0921985047cf940070b0c61a82225fc742aa4a2e3', u'161400e37071b7096ca6746e9aa388e256d2fe8816cec49cdd73de82f9dae15d', u'af355fbfcf63b67a219de308227dca5c2905c47331a8233613e7f7ac4bacc875', u'1c433a2359318372a859c94ace4cd2b1d5f565ae2c8496ef8255e098c710b9d4', u'49e09d2f48a8f11e13864f7daca8c6b1189507511a743149e16e16bca1858f80', u'5fd034ffd19cda72a78f7bacfd7d9b7b0bc64bc2d3135382db29238aa4d3dd03', u'74ab68a617c8419e6cbae05019a2c81fea6439e233550e5257d9411677845f34', u'df2650bdfcb4efe5726269148828ac18e2a1990c15f7d01d572252656421e896', u'1501aa1dbcada110009fe09e9cec5820fce07e4178af45869358651db4e2b282', u'41f96bb7e58018722c4d0dae2f6f4381bb1d461d3a61eac8b77ffe274b535292', u'aaf9b4e66d5dadb4b4f1107750a18e705ce4b4683e161eb3b1eaa04734218356', u'56639831c523b68cac6848f51d2b39e062ab5ff0b6f2a7dea33765f8e049b0b2', u'3a86f1f34e5d4f8cded3f8b22d6fe4b5741247be7ed164ca140bdb18c9ea7f45', u'da0322e4b634ec8dac5f9b173a2fe7f6e18e5220a27834625a0cfe6d0680c6e8', u'f5d94d46d68a6e953356499eb5d962e2a65193cce160af40200ab1c43228752e', u'e725d4efd42d1213824c698ef4172cdbab683fe9c9170cc6ca552f52244806f6', u'e7711581f7f9028f8f8b915fa0ddb091baade88036bf6f309e2d802043c3231d']
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, 1)

        ethBal = self.s.block.get_balance(addrSender)
        res = self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=keySender, value=INIT_FEE_VERIFY_TX, profiling=True)
        assert res['output'] == 0  # verify fails but not the point of this test

        totalEthFee = INIT_FEE_VERIFY_TX
        assert self.s.block.get_balance(addrSender) == ethBal - INIT_FEE_VERIFY_TX
        assert self.s.block.get_balance(self.c.address) == INIT_FEE_VERIFY_TX

        #
        # twoSender cashes out ALL and should get 1/3 of the ETH fees
        #
        twoBalEth = self.s.block.get_balance(twoSender.addr)
        contractTokenBal = self.xcoin.coinBalanceOf(self.c.address)

        self.s.block.coinbase = twoSender.addr
        self.xcoin.approveOnce(self.c.address, twoSender.expCoins, sender=twoSender.key)
        self.c.cashOut(twoSender.expCoins, sender=twoSender.key)  # cashes out ALL
        self.s.block.coinbase = addrSender
        # coinbase dance needed so that balances are as expected
        assert self.xcoin.coinBalanceOf(twoSender.addr) == 0
        contractTokenBal += twoSender.expCoins
        assert self.xcoin.coinBalanceOf(self.c.address) == contractTokenBal
        ethGrant = totalEthFee / 3
        assert self.s.block.get_balance(twoSender.addr) == twoBalEth + ethGrant

        totalEthFee -= ethGrant
        assert self.s.block.get_balance(self.c.address) == totalEthFee

        #
        # oneSender now has 100% of issued tokens
        # oneSender cashes out HALF of their tokens and should get
        # 1/2 of the ETH fees
        #
        oneBalEth = self.s.block.get_balance(oneSender.addr)

        self.s.block.coinbase = oneSender.addr
        self.xcoin.approveOnce(self.c.address, oneSender.expCoins/2, sender=oneSender.key)
        self.c.cashOut(oneSender.expCoins/2, sender=oneSender.key)  # cashes out HALF
        self.s.block.coinbase = addrSender
        # coinbase dance needed so that balances are as expected
        assert self.xcoin.coinBalanceOf(oneSender.addr) == oneSender.expCoins/2
        contractTokenBal += oneSender.expCoins/2
        assert self.xcoin.coinBalanceOf(self.c.address) == contractTokenBal
        ethGrant = totalEthFee / 2
        assert self.s.block.get_balance(oneSender.addr) == oneBalEth + ethGrant

        totalEthFee -= ethGrant
        assert self.s.block.get_balance(self.c.address) == totalEthFee

        #
        # oneSender cashes out ALL tokens and should get all ETH fees
        #
        oneSenderCoins = oneSender.expCoins / 2  # oneSender only has half their tokens left
        oneBalEth = self.s.block.get_balance(oneSender.addr)

        self.s.block.coinbase = oneSender.addr
        self.xcoin.approveOnce(self.c.address, oneSenderCoins, sender=oneSender.key)
        self.c.cashOut(oneSenderCoins, sender=oneSender.key)  # cashes out ALL
        self.s.block.coinbase = addrSender
        # coinbase dance needed so that balances are as expected
        assert self.xcoin.coinBalanceOf(oneSender.addr) == 0
        contractTokenBal += oneSenderCoins
        assert self.xcoin.coinBalanceOf(self.c.address) == contractTokenBal
        ethGrant = totalEthFee
        assert self.s.block.get_balance(oneSender.addr) == oneBalEth + ethGrant

        totalEthFee -= ethGrant
        assert self.s.block.get_balance(self.c.address) == totalEthFee


    def testEndowment(self):
        assert self.xcoin.coinBalanceOf(self.c.address) == TOKEN_ENDOWMENT


    # based on test_btcBulkStoreHeaders bulkStore10From300K
    def bulkStoreFrom300K(self, numHeader, keySender, addrSender):
        startBlockNum = 300000

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.setInitialParent(block300kPrev, startBlockNum-1, 1)

        strings = ""
        i = 1
        with open("test/headers/100from300k.txt") as f:
            for header in f:
                strings += header[:-1]  # [:-1] to remove trailing \n
                if i==numHeader:
                    break
                i += 1

        headerBins = strings.decode('hex')

        res = self.c.bulkStoreHeader(headerBins, numHeader, sender=keySender, profiling=True)

        print('GAS: '+str(res['gas']))
        assert res['output'] == numHeader-1 + startBlockNum

        expCoinsOfSender = numHeader*REWARD_PER_HEADER
        assert self.xcoin.coinBalanceOf(addrSender) == expCoinsOfSender

        # block 300000
        header = {'nonce': 222771801, 'hash': u'000000000000000082ccf8f1557c5d40b21edabb18d2d691cfbf87118bac7254', 'timestamp': 1399703554, 'merkle_root': u'915c887a2d9ec3f566a648bedcf4ed30d0988e22268cfe43ab5b0cf8638999d3', 'version': 2, 'prevhash': u'000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e', 'bits': 419465580}
        hashes = [u'b39fa6c39b99683ac8f456721b270786c627ecb246700888315991877024b983', u'7301b595279ece985f0c415e420e425451fcf7f684fcce087ba14d10ffec1121', u'6961d06e4a921834bbf729a94d7ab423b18ddd92e5ce9661b7b871d852f1db74', u'85e72c0814597ec52d2d178b7125af0e3cfa07821912ca81bf4b1fbe4b4b70f2', u'25ca9ce6e118225fd0e95febe6d835cdb95bf9e57aa2ca99ea2f140a86ca334f', u'a52997fa37fee82c0bf16638f5ec66bb0df999034c6b21bf9b8747c1abed994f', u'dd9aaf33afe6f8364a190904afcc5004fd973527be5a23f68bd7b6bd40f84c59', u'83ff2b04fe5e19f2650c5fedc706a26ab314e9edc40aed106373adaa36f6bf12', u'3c412d497cb5d83fff8270062e9fe6c1fba147eed156887081dddfcc117e854c', u'5a0ce1166ff8e6800416b1aa25f1577e233f230bd21204a6505fa6ee5a9c5fc6', u'3184aa6ccaed5f3e41fc34045970cee7501b68795c235108debd1c9a5dfec1a4', u'80bf2f098684a5db1ce0b14c0adc75efec6710a040eacfb81f64917c34e69ca5', u'80f6247937daa9ffd866e616abd337177d734a35f847669c41ec358817f3a7e8', u'3f4735eb3beb164150000b90fba6055bcff7a08ecba9352b7d29f404a658d2c9', u'c33240a15d4e252ec0284e4079776843780a7ea8836bd91f8fb8217ca23eed9b', u'15796981d90b9ecbce09a9e8a7b4f447566f2f859b808f4e940fb3b6ac17d3d5', u'60e9a2b1f7120d329fd41f1b48f5f1b3a3a581212bec241fd8f1f2a37a06efeb', u'b31214324f4c4d59540346de6cb692c02fdd31674486bff4981a8a7d8db74b6e', u'8cd58bdc6b27fd9b664e2499e9ae7d8fd8ab61757a14e9face89b1d3ce72e8d4', u'430116ff8ba9331cd0aee2530841661a9f138655eb3f013cb159d4387a5c8d75', u'07985ed09f592d6a5d87f20631f31f0e844a63eb6fdca293be5b8cdd966b5bc3', u'05cea126741dcc14e8b04a71c7b3a20790ac650a34c2af3d26ad591897a745bb', u'697699797160497048258d35a491929772d3afdb4d39e2f3b1215f69f34f95e4', u'83088c0ad83575d56013dffe44a6820d5931ec7b2df0a72a7008123714541230', u'f14255e8fa5618b03a6f99dff6c0635f565278dd951d776daa392ef8a22314cf', u'81335877f5ba07432f642206de7bb30367e3da8fa48dc91139795ecb6571e39e', u'3a87b229b9db4a9562d1453106f7b61aa67e05631cf1068cf37af910101c1b7d', u'4f4c7d7e0677f5109cc91287a7635ffb4906dc91d1287f0d8661cec0e2dcdbaa', u'0c3570cc17b033ca526fb06e3d9945aab06b279c11aee3e947a6f76b9d938cad', u'e9ce733b8397a3e39ed484e2766095e2cc3fb80e62e6c01281223d4e98516125', u'7711457b2611b68b0dd03291cbad3e56015233f7861cf087686ac8b7a6bcd2a1', u'3b4eaaa4c92e5e79f2a2b5a91517290a8134b0581cb5146b5bb34abb2da6105a', u'4d4a6f9408042e48cfd78a0151c8e01aaec829a6bd0154c9aff8020fedb19910', u'200f10f9a80042bc2ea3ce10678a22c2f2f65e8c9eb77cb02616ab994d78bc64', u'9fa29ce548cdc746ebfca93778a13f2aec7ca337b3713a508371cc895926c4e1', u'38a7fb461f35590b1b637accc0bc7cfbd8dc97cd29494f91f6de7ab650b77662', u'692229d9ddcac96288015bbbf9ef2ff21ea1f332c258ac09d67ea90a89643e1e', u'cbad0a4ee0b505a4b004e1ec9e8d845ffaab9fe006841a5de0f57f45975f638d', u'fd0fe9667036af10d633674cdd216b8f3dfe8dea8530c29735bb8494ded454d3', u'73eee43d7fd9ab2d38323a25ee776f79dd05e37e0bac5c58c3537fdf8bebb03a', u'dbb2f7d327e746cc5271f0184446319d13fdab43f7cd9c9bdb1780fb51333195', u'bb420523868848e1b60ffe28a2f5a657e7db424e11aaacca19c992eb67805349', u'd826449f965893e8a9e16e7c5eab237250167623bc2464a146bca66fa17bc859', u'a258557069b65f7376a0b183b113d09a6488998ab3b37f3b22e653064673a4f9', u'ac4e61fab92d01541734295dd8b47647989b696282d94f7e03f3d517a2c8fe0f', u'14778e8e4f139ea8d3802c9390f95d762748acd44af0bd5f990ff96254694539', u'cd127347cb166b6dc07b54e9a1212122b965116f44f64c8a181e0f1ed13a7a94', u'e9eed99ee6ad90d43fbcf01fba43c644f0d1267b7821f252ee796a29772a9da0', u'160b3ac2c0e8554a4693f618099027c183ca8528f16bca39bdf594f012e0d259', u'8d3c7ac9c640836e344dda3b2d8969d674e203cc85e1b42b364b9cd379bbc54c', u'4d493d0803f6f66755f2527c09bde9e37cf829e036f2a408c0ad40e981011808', u'ee170c8b853905e267e046da730de4efc5924b9d45a138703962bd88a427841e', u'014150195ba681ac08be9773d01cebea757139c262381b83b68505b0865df37f', u'7f3717dfb7530b2ac2f3d5891872a80616c0c9114cb813123151ef604fcec2c8', u'bac470d551be0ddcf575f6241692a059029e554b3bd759e29cb582df2c452ef1', u'f902e9c1e85fbbb970a68c54f07793b82441341cb84edfeeddbc5008dd3fa42a', u'5c42701ec8b6fa449e294c063d63a1378a82335892d8a968867e507456d6dd46', u'eec726af5ba61dfc183f23e2561af3dbc72e17567e63de8919c383aed0b34789', u'e8c8ffe8259fb98535ba4b3028b3d15726ccec383a263bfb47735d614aa1c8c5', u'79d57b6337a02b36e7fb341da626cd3f641f4393b35ad750da1f18710ec7132a', u'32e19411618c67afc97dc6ecb188d9d3a7c179ba652191f52d019a1db85eaa39', u'ef2ba16f90b39a6982df6f70600d683529d328a8b88d5f03cd9611ad2c67d898', u'313ef3fcf6a27a5cc376422e10a7a3c835aa5cce098ca206d35998f1f950907f', u'bb727c8f9cc138ec17a36355473b902f8170b415e62b537c9d9514a29b18195b', u'bd89b3e925e1a98cdfc323e27cd096f331bb8b61dce58e55277418acd4e6b81c', u'eab98223941ddf74dc5f24c50c18c94fe37de0b976ae57cf12877d2adea492c7', u'59157efb4c7ffd44d76c9e26f2aab16288d408caa821ed6840312984cab397c2', u'4a4343f87d0a15583b738447d4b252d29ec6014b364f75a6b82febdc85f77d36', u'bd2fe3c72fdff8ff934195bfbec9efde589eecc7e2486d1a27137490b934f0bb', u'5a73af81efbf315df6db9eda21e52c45462da2c2f4d9cdaa0aabaedafbe5a0c3', u'01df07dd63c90be88c2c6fdb7499f26f6af085cb9aaa71ef4a896abc7619c5e7', u'2eec110d8d89c01952cf48e71ea297c039eff7536034ebc5e6b2635d6125a636', u'93f0a25cb92a4fdde230335d8236b21309375800bfd114bad79d2b78a741b236', u'9a597af7f8cd737115368afde26fa3ddbd61f1852a30896d146b003bd96c0e28', u'6aba765dd5c019b226789bc4bcd69f27819161765d2264e231bd43afa31d5329', u'67230ecd856ea2a271d11a20e7686b8a1d8ea17b8ee39deb4999d8742619c287', u'81df42b9d145c7306aa363069bbb5dfc39f27169ba4cc0c0fe05fe957a40d5ed', u'2079d746f4ba56140cfd5ff6e8d870c7798cfa08c83984e726614ee9fe09636d', u'6eacf3862e3d96b06269971ce96e955d87e1eb036156d0f32a25dbdd83bf9ad6', u'f9a6c8c0a9d9104925b826c2f88be0e39701e2ed609a0047dff77b758427c967', u'e1822ccb952aff1d5453081116cab5dd193aa01012265153e20073b574559fc5', u'67616a53c479b20693ef82bc61b0f1d3dd6219b7b39eba3adf849666ac269d31', u'6ac0be3b5fe96e5aab1a68b073ec47ef281e4b9f1757565182a10b4d969ad979', u'c955e04d7d129735914785506fe945edcc11afdcbfff5f0c145eca5989d1ba9d', u'8bff2d6bd3371ab20b3025d017f98c7830360cdc138f8949636a375ad862ad5a', u'0c6b4796eb26bd092bc99d2f71100d15de77e9ab89d878d10940610221756e4d', u'f290713ba603832d71bd1cb055b275cbdc112bbb773079ae208adf9376ad4d8b', u'54929ba3c1b9a6a96e67a17c0ba7c63322a8852d6cba771fb8c18c6964b352d0', u'dd91af04b80457a741d0e02e4d5d9199fbca7eafc173a9db9c0c8ac39e575f4a', u'c08deba97b231b535e843a30b25ea5e82ac84b0dde44315fada98eec0e5fe0f5', u'187eb5e2503c24afbdd396c113262cfcf9a8b48ed64476f36705c9d2a14b6a1f', u'a891400adcff3db30dae2a5e6d57399c84a9467bfe5b1f8040ed3861f91413e9', u'0f771706adf8399f088489917251174402107d92bc0d28fdfdcfa48ad2b37429', u'9f12792e30797baf6a25f3128e4d89c8ffd46b667c2391a5cafeb5a8817a4118', u'd74ed5ef608c251f8ae1b06b6ca5e20ed365b96399c70a2973d03596b97ca1a8', u'6621d46781aae5ea3aea9016b517196bc8a39b4d2412dbe8ec37f148c841f992', u'b2f15a79fdb8b77966089eb53f3a7950ff5de9f0a79f0883600cc2b545b42491', u'cebe405a224b64774a9b394620c83fde847511d92145cbdc1459de2cadb93e50', u'1d2f946d69b5f48ea84dd4ed30f468126bc3d605d737d14151e7b144863e9ed6', u'dfe4429838aaff73694700a1ac2de0f18b4cc9c5c350525b0528769718a76ac2', u'd398d7ec7d847be58f32ccebb90c9a1489b51b8f02dd3ca69bd43e6695ea01ba', u'1272c9e1e3acf67ca2359076a6eb5d2ee81632ee4720b1abd18e206cf2ba58e8', u'0a8d85932d7acf42b175ce94785732db179946678f42b91bd8ea12834f5732d4', u'b0f72f99a1b8155f4e08aa5fd7b7bf1ef6a724c9f17e3b99ab3d732a66903514', u'a1be755bfc1d7bac848231bc54a0bfad250441cb0841ba5c37ef55a26ea0ffa7', u'293d0d15766fac48b94b2cf188b5bd5d53c640749f65efc747554bcc03aa6577', u'3af197c25dc773bd09b6b2f36bca282a14ddf00922a570606214bf3180bb8420', u'2ec52b1c0c312e28790a2b88014cd2bba7a8ec06902aeed321dac8b7c9098cb2', u'fabef88911c58225014d5758dd59e46916a9a122848d8c7fa8230197afc8849d', u'140d297a04eeb94a464db48da32efe7801dba32c6ecb5411c9057bb32e4f2955', u'6ec656b73c7d04e7bbc3fcefc7359c91b74040cc79fc21cfd247bef2d230f73a', u'bdae0e5dfa9f494413586dd8aca440b0bbea849a8cd9c2342ec1f27e320b971d', u'691ae0704e080e04411ebca008ce1b7ff4a05f8b67f6da2ee8aca0f32657c50e', u'e6cd0bf28ad5f512f5fdcb65b053b1662f562b3734bfc17ac952af892a767df8', u'df244e11f1bd63cc0c28073c1bb418daa8a1f7da67e6e2e7b140e2f05c8450c3', u'60ee29e4256ea0b275e6b230a531cf40f348277dd3e118948365d11cac4d9131', u'f8c9b22b2cc94966cf47e5be1c3dbc54a6e3619c08b6b957339159a504c97804', u'702451ad78d73bd3a3b3793049d6382a819750177648a0429da49b485d842173', u'45cac6176a75416c666aad603ec085e0948beae98539791a6bfec69fa5e241ac', u'0bceb62c2fe23caf701800f24e44f0278838bac015f7567f8dbfdc4d3a49d093', u'7360377a882c923bb415583777cf0b340a4fffc63350c53891564b4955976b7e', u'22d5669af43229adfcf2157de9477b013265d6fd70b1cacf7048457c65243fe4', u'c36bb17c97ebd644fc7ab9362b2d04ad63c9fae8c7f9047199c1d408df419913', u'556d7c72dd4636a5cba7fc3dedf57cb34555bf913dc09e187bdcb489c3804726', u'e48b08df0afa01a7339335fb6b6964100d11985765cbc6afcde990fd65856a9b', u'9cc064bbce74a2c56ce12b0b59fc7267a2618a35e1d8c66f642efd6d033a9681', u'12998f415cefa518a76278d82d6088d7aa512c2a1a8c3e91d826aa415c809992', u'e8b85649bdf57c0927c2f36486f1147c53ae153a2e3d6cbab1cf238d8ab65e7b', u'fafe668f8725ad2df033f3e5f86a793ac23a58283d992c1a0ff610579b56362a', u'd111d3a9bd8f499946309764effcd6bd7f1b1bb0f7f1d5562ecb88ede72bff31', u'8bec816469f65b34cc517d65b69dadc7f94fa3e19c5e34ce66351d6bd76d46b8', u'a0dbb7cf37e49483be11ce690c7c4333bd50d47df3194efcc29f141fb37e1d16', u'2855f1cf7548aad0ba6d865d9c97c95f0c7bf8dc65af38df49ad74835bc7c937', u'fa571daf7590ae943afd2b6c9072b5a47864d4e4d2055c3b4acb4ac1343c48e3', u'34d5c5fe77e6869b1b383637d058a33946dbe103edc927a0e38d26545aec8d9e', u'f87c866a8782370f004070ae1caf8b91323f1c93186a76024d439127dcd87c1a', u'2b1a908eaa8add861703d10976e64ac7946c8b83be65d66c2de4bcbac4e3cb4e', u'fea520c626ab8832451e589a4e430723a70157de7bdfbda10b61b0c618c2744f', u'1f5bbe466a99c2f75a7bc126372f56323abeaa2c2b66f972745cf153194dd71f', u'af3fcfa1440bc4d40436c69ca1d63d3bee61ffd7f41124e58a8eeac371ef9876', u'e8c5e36001052efaa2b5df0b28457002887ae73b6e49ce77f4229ad0e04a5caa', u'2865ec584fa147a52c644b744f8044502d3625e7637b55fc43f42533f3918791', u'c574cbf9ee51c461ad7b1a946760df0e996c174e331ec7c0d3ae1818d38442e2', u'f7f96a71f0e33be4665f8856b89549d46f663a1f5d5ca91efa10b0d2ee969a1a', u'ece6636a6afb756930b25915fd71940f8cb0f398348866a73cd100ddf54774e7', u'1a1ae6e74af37afbb8ed812f779cb505410f439b380d08c33832fb7291e4fa3d', u'86c7d896023f918da17cbc411110999e094b0c9434e457711eb54c56ca7b7786', u'f2f814c488de5382fcca21deabac38cc7aabdbdc9eff28131a426b9c09069e56', u'c567df44fa6c0a613394524943c2a01258da8e7f7fe532cc2bb3a2176f202c74', u'dd26818f759d5566ad3de82bfee739d138ba55e4d46315fbef4f5f4c000aa8b1', u'20cf5a1ff51f2c4ccb7e842b09238167e1951be18f409439ba7d0b074a9aa035', u'0842b84421b9f010ef4390fb70e7fd0e25a868bf3823822f168c49a0247ba552', u'62650f017ac2eb9c75a0544d992c527062823d579108545cb2a5479fb359b8a9', u'543153fff73eb3a86f7d33934889aded91626e2ddd8d6391cfd3183f94467057', u'c699b2e258c8f2659dd6288f303929485c03093b9b195b76ad2a72dc1942aff4', u'5f8ee140aa6e9458d8cc98fd04de577d9f1d5f7ba22d1aaea9dbf18d29f4aad5', u'195624d25e16e2f21477c0e944dadbd8562eb95d7d6f02a10eb9d1706ccd6be0', u'9f8a4be4106745a1c9615c24dcb33e676fc20b263b790dcc5938bd25c9cfa7b6', u'c61d7b9e7f27c88c90cb88cf5c14cd2733dfa126ca916c967b5425e13d6dbef2', u'fcc5e7327547595acec6d5496dbb7047bbd3d7bef15d8a99614507791a0e919c', u'12e58986ff3f692e1d9811d4b7504f9ab12a8328d01cb384561372a8977fcb4f', u'36bf83edfee9780bf71d5ae2e5564682c093ee856e0df242df68cf36f636cde3', u'7aa7d8dc67d83997271055fad15ba87439caca44cb887d8494e2e3d7a035489e', u'6bcc5699a9d768e7c32a7cbacecf4e04c0a3b47664435e85c267f35e62b34a40', u'464ce88d4978fd2aeb1d07b9859cf4bbc7d64835da34c8908a422cd69b05764d', u'4081f9bc98d0fe6c1be648ba58d3038f178d367033d5504826d89dc01b641883', u'8fddc291012eec652f89ec544c25a62d5c7b56485cb62aa84b4cdd1e5b9bc6e3', u'4ea733208b1287b4b6158f40631dca4aea9003cfca273593efe7c55fbc2ac93b', u'26327d0878a2e51007bc4f6f8eb731729a6ece8c0c749d0b0462b7d27ed9dec4', u'79e6e69805cf4148decdb67fb230242f176456070e989fbba170a202ae6e8be0', u'5f706df8103ee22d87715c5d766af8a965c9f3d3ab393663acecd1a88f9e5732', u'5ee987ebefa35b7a7ee95e5239fc04f5777e6b5e290c056174d87636d388d783', u'173f27313b60ead70171fbd0ab755c7d6e40d1336f1c427d34bf138615121a64', u'c29fd604274e072c2bd4a879dcfa516b5c8d278a2123bcdd58d52b9040353137', u'e4655d09893a5b5d96fc911aa73140a67f8ccdb43354522f125706e7f0a9c3f2', u'31f27a1e742f9590c4a3b2a9c6e95d44f265cb328d52cc0dcb17a133920a84b1', u'1f5dff66b173bce3eb9899a2e03525e0ce4ce26d21b311c11361df9c097bf4ab', u'94bf9d213499a3dbb6938c81f92a7584a9d74912534519f7372548477eb582e2', u'fcaa773d66d90f0509375bf9fd47fdb665b215959095b140d30ebc07435f6672', u'9b3cbace712f1fef331b91a4a557395d771c00f177f286276d8f039a4f508837', u'7cf112ba96c4999533ca3f2d27b3b7580ec90658918d10cb4f161ec35102a815', u'91fbee07653d38151b3ac628624716c7ed0822245335368b4cffdafdfddba2a4', u'8b516fc42ee3cfe729559e53df509aac06f2d2ea67b4198d75f50ba57968556f', u'fabf8e33fdcc6d874a2799d2006286f7584a9e4b6962271df7183f7f40c801fa', u'42afd1587aeaff52e62569d8ba87a26839e2c0213ace92518fd0762dd52b00e2', u'e4962898a6f3c54337f38ce9e941092748f1d16aa214fa8094b0fc7b643c6d25', u'f071a9340dcc73755a775083bb1cf50f7c4ce43afc0faeabae324c47c74b506b', u'50cf012c35ad0a5f38506fa510e81122e1db8942916c71ed3ab09ed81ec2322b', u'fa67048a1d19de38779d9a784980f1fbbc2cffac51e9cf2eb5428cf50463e173', u'7f55b1be49234705fe38c0b20b21bb8b80ebeef7caa115e59163f732c93abadf', u'141e4ea2fa3c9bf9984d03ff081d21555f8ccc7a528326cea96221ca6d476566', u'09636b32593267f1aec7cf7ac36b6a51b8ef158f5648d1d27882492b7908ca2e', u'5bf2fc8b3d5fd649104ea4a0996a263a22d9a27bb8bbf7c5620ddfa59180415d', u'bb98981ae53448e37f9f9b92308532ebbaf2cbe1cf678971b3c48f8556e3bace', u'4507c1c9eb8898e959fe563f26410f74ee898f57e799fce6d2bb3c9e7768d2e0', u'45f347c4811a168cb9a517b1a67f4c27ceeefa0d6fe92b62f4f32023282759c1', u'8b8bb1e04c132542b2e4fec124bbf1587e8206e635ada0c5bc77adc84a69d71c', u'8f05b10b8bcd0f9c646133c2a6c2b862b987d4bab1fc543e203d225f51d332f2', u'92951b259f6f50af6b0c9615b02f4cd32adaa68b44b0a1f341e51b8d066f7242', u'8c2c452e01c8e1fedcce515d8eeaeb554fb8d3a9199c8f7487b43f97dff78b24', u'b3a8743a49ebc07d51063f05cfee21e0550c88bd066ba4848d3407d3b83caa67', u'6bf1e0eaacd3a028314404fcf7070857718d9d6b1effef8ae30b1dd12daeecc0', u'4de44365c2d8cccc47146eddc30a3ce1c0f3cf2f02a76d5bc448ab9df8e9a50a', u'a7fa6bb651795f601bc5b30d46f2ebc54c1f4e64660ba3e2c9aa4ff67b5b2b44', u'0f22eceac6512674cefc616ec02e8602e39b7988335d354b4b9e46b202a4d1e6', u'076c4630f3233c40f2d081ca5205c0511e3ae151a843d07a241a367efc459d8a', u'381c90c62d292e883a9954f4cb30910a22a2ecf623f81c479e3bb62c076ae15c', u'f2b36993c8b6954a49fc8101a5a73be1c12e1dc54607e4155f6cc89050dcdc3f', u'17e92b3249912210d734ea870724e5aa89d14fdac19775c6f3fb27b0443b578f', u'df9d82e7d64773876cba3f238d3314156a9c047bea43f74b3d333e58e32c02e8', u'1f001521ff4d15c9cf5e0573b7626089f0fc3adc80f3a95efe27a5bf11d42cdc', u'fc15cc1b201179302bb865ad94157dab220200feca696db1719b6305ce438caf', u'af5a9d4881abbb86176fec8f19b70e2bec2ba331e55660c84a65ae56858f2140', u'b4fcb470c50bb9de902d78b068ff8fcbd43f2a703405f12c67c33b8f0d142333', u'7e59df63b51452499b8e8916e077e1a8b031ff2a3578fa7362d6b8847fb0b087', u'8e3c4705b993a7b62088586e8ad07d4d53dbca75cf3d7dcfaed856b0724a9e36', u'8ad2f603082827e24cabf1079e90216d5c0ad9071cf326a88625ac22fd654635', u'686ffa6fa20cb99f5b66741546e854363569d6b6557481d41947b5b4243e02a1', u'278d14dbae58d976299144c063727c0d8608b2df09d1d6f98d08dcd016db1d3f', u'f2486038276fe29dad82f1c163119b01c33638a2699ab7c0e97a6c4a1d7ecc14', u'83e276a9ab6d8936435e222d0dbd25bfce1b6a05e25d3cb311ca800aebe26cc3', u'ea81826abb33c8e2001daa1adf1d807d958cb007422cc77c1873cf302bd338b3', u'b6c73b487847f9f23716dd4aa37572d0ef33a061e5763a5277dafc1e09c0804a', u'edab80d85ad6cb79c42eb909d36031268cf801b79d70c3aa314e9485b8aeb071', u'8570dece43243e0e648edf63803c4c4a92ef2f84085db5219c2d932a80f6c68c', u'64d02bff2385b2406bcce5084cffffcf2b251ad19cf2da353a83a01eaf248907', u'ba7e4f59b925eddd31c349392ab92655e30ea41f66b90441ac190310f05f8eea', u'2f637d397e7a7f475b31d7cbac564ffc52ff7a2e826590c1a07b67c863e819dc', u'10d3aa0309d9f6ac4a58a75563ca49667965b6a9f454eef10b024b5f91eb030f', u'446249cf6bd83ee255cae174194a03e9c653648f219eed3a9d0edffd1892ce19', u'07fa53991a585d45fef3d8434a4004c56e335a936efc8fb77776481c9fdd88ea', u'9aa48344a6f4d316c0be11d3591c4a0597af167bc68208234ed479f71486a5b4', u'e0c4a881e591e1d05000443821b0c524c81236ea4248f39985635afade584166', u'75a98ce35b869772adbf643b3f8acadfa5b46b4cd8bfef26f9e079c517018285', u'e67f95cd4d5682f2b9d4e19b658baae692d669e550e6e3337c07d7395800c5a9', u'9a23b701a614b81746c0a44caa8b393844f94aaa8a13b57666a6813464e72f94', u'3b115dcc8a5d1ae060b9be8bdfc697155f6cf40f10bbfb8ab22d14306a9828cb']

        return [header, hashes]

    # based on test_btcBulkStoreHeaders checkRelay
    def checkRelay(self, txStr, txIndex, btcAddr, hh, numHeader, keySender, addrSender):
        [header, hashes] = hh
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, txIndex)

        # verify the proof and then hand the proof to the btc-eth contract, which will check
        # the tx outputs and send ether as appropriate
        BTC_ETH = self.s.abi_contract(self.BTC_ETH_CONTRACT, endowment=2000*self.ETHER, sender=tester.k1)
        assert BTC_ETH.setTrustedBtcRelay(self.c.address, sender=tester.k1) == 1
        assert BTC_ETH.testingonlySetBtcAddr(btcAddr, sender=tester.k1) == 1


        eventArr = []
        self.s.block.log_listeners.append(lambda x: eventArr.append(self.c._translator.listen(x)))


        ethBal = self.s.block.get_balance(addrSender)
        res = self.c.relayTx(txStr, txHash, txIndex, siblings, txBlockHash, BTC_ETH.address, sender=keySender, value=TOTAL_FEE_RELAY_TX, profiling=True)


        assert eventArr[0] == {'_event_type': 'ethPayment'}
        eventArr.pop()


        indexOfBtcAddr = txStr.find(format(btcAddr, 'x'))
        ethAddrBin = txStr[indexOfBtcAddr+68:indexOfBtcAddr+108].decode('hex') # assumes ether addr is after btcAddr
        print('@@@@ ethAddrHex: '+ethAddrBin.encode('hex'))
        userEthBalance = self.s.block.get_balance(ethAddrBin)
        print('USER ETH BALANCE: '+str(userEthBalance))
        expEtherBalance = 13
        assert userEthBalance == expEtherBalance
        assert res['output'] == 1  # ether was transferred

        assert self.s.block.get_balance(addrSender) == ethBal - TOTAL_FEE_RELAY_TX
        assert self.s.block.get_balance(self.c.address) == TOTAL_FEE_RELAY_TX


    def storeHeadersFrom300K(self, numHeader, keySender, addrSender):
        startBlockNum = 300000

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.setInitialParent(block300kPrev, startBlockNum-1, 1)

        expCoinsOfSender = 0
        i = 1
        feeVTX = INIT_FEE_VERIFY_TX
        with open("test/headers/100from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeBlockHeader(header[:-1].decode('hex'), sender=keySender)  # [:-1] to remove \n
                assert res == i-1+startBlockNum

                expCoinsOfSender += REWARD_PER_HEADER
                assert self.xcoin.coinBalanceOf(addrSender) == expCoinsOfSender
                assert self.xcoin.coinBalanceOf(self.c.address) == TOKEN_ENDOWMENT - expCoinsOfSender

                # http://stackoverflow.com/questions/19919387/in-python-what-is-a-good-way-to-round-towards-zero-in-integer-division
                feeVTX += int((feeVTX * -128.0) / (127*1024))

                if i==numHeader:
                    break
                i += 1

            endTime = datetime.now().time()

        assert self.c.getFeeVerifyTx() == feeVTX

        # duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        # print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))


def initBtcRelayTokens(cls, tester):
    tfAddr = cls.s.evm(TOKEN_FACTORY_EVM.decode('hex'))
    _abi = TOKEN_FACTORY_ABI
    TOKEN_FACTORY = tester.ABIContract(cls.s, _abi, tfAddr, listen=True, log_listener=None)

    tokenContractAddr = cls.c.initTokenContract(TOKEN_FACTORY.address)

    _abi = TOKEN_CONTRACT_ABI
    _address = hex(tokenContractAddr)[2:-1].decode('hex')
    cls.xcoin = tester.ABIContract(cls.s, _abi, _address, listen=True, log_listener=None)

    assert cls.c.getTokenContract() == tokenContractAddr
