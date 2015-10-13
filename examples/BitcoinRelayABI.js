[{u'inputs': [{u'type': u'int256', u'name': u'txHash'}, {u'type': u'int256', u'name': u'txIndex'}, {u'type': u'int256[]', u'name': u'sibling'}], u'type': u'function', u'name': u'computeMerkle(int256,int256,int256[])', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [], u'type': u'function', u'name': u'getAverageBlockDifficulty()', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'int256', u'name': u'blockHeight'}], u'type': u'function', u'name': u'getBlockHash(int256)', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'int256', u'name': u'blockHash'}], u'type': u'function', u'name': u'getBlockHeader(int256)', u'outputs': [{u'type': u'bytes', u'name': u'out'}]}, {u'inputs': [], u'type': u'function', u'name': u'getBlockchainHead()', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [], u'type': u'function', u'name': u'getCumulativeDifficulty()', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [], u'type': u'function', u'name': u'getLastBlockHeight()', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'int256', u'name': u'txBlockHash'}], u'type': u'function', u'name': u'inMainChain(int256)', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'bytes', u'name': u'txStr'}, {u'type': u'int256', u'name': u'txHash'}, {u'type': u'int256', u'name': u'txIndex'}, {u'type': u'int256[]', u'name': u'sibling'}, {u'type': u'int256', u'name': u'txBlockHash'}, {u'type': u'int256', u'name': u'contract'}], u'type': u'function', u'name': u'relayTx(bytes,int256,int256,int256[],int256,int256)', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'int256', u'name': u'blockHash'}, {u'type': u'int256', u'name': u'height'}, {u'type': u'int256', u'name': u'cumulativeDifficulty'}], u'type': u'function', u'name': u'setInitialParent(int256,int256,int256)', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'bytes', u'name': u'blockHeaderBytes'}], u'type': u'function', u'name': u'storeBlockHeader(bytes)', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'int256', u'name': u'txHash'}, {u'type': u'int256', u'name': u'txIndex'}, {u'type': u'int256[]', u'name': u'sibling'}, {u'type': u'int256', u'name': u'txBlockHash'}], u'type': u'function', u'name': u'verifyTx(int256,int256,int256[],int256)', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'type': u'int256', u'name': u'txBlockHash'}], u'type': u'function', u'name': u'within6Confirms(int256)', u'outputs': [{u'type': u'int256', u'name': u'out'}]}, {u'inputs': [{u'indexed': True, u'type': u'int256', u'name': u'errCode'}], u'type': u'event', u'name': u'failure(int256)'}]
