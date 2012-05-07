__doc__ = '''

A demo of how to use the MCP system, as well as a unit test.
Note that this is a sorta silly demo since both gears/clients
are running in the same process and the same MCP router.

### Setting up communication

>>> from ConcurrenTree.model.mcp import engine
>>> e = engine.Engine()
>>> gbob = e.make('bob','')
>>> gbrg = e.make('bridget','')
>>> gbob.host_table
w<{'content': {}, 'routing': {}}>
>>> gbrg.host_table
w<{'content': {}, 'routing': {}}>
>>> localip = '127.0.0.1'
>>> bob = ['udp4', [localip, 3939], "bob"]
>>> bridget = ['udp4', [localip, 3940], "bridget"]
>>> gbrg.client(bridget, ["rotate", 7]) #doctest: +ELLIPSIS
<ConcurrenTree.model.mcp.client.SimpleClient object at 0x...>
>>> gbob.client(bob, ["rotate", 3]) #doctest: +ELLIPSIS
<ConcurrenTree.model.mcp.client.SimpleClient object at 0x...>
'''
