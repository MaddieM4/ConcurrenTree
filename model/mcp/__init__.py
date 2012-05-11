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

>>> gbrg.resolve_set(bob, ["rotate", 3])
>>> gbrg.hello(bob)

>>> gbrg.dm(bob, "Hello, Bob!")
Direct message from [u'udp4', [u'127.0.0.1', 3940], u'bridget']
u'Hello, Bob!'
>>> gbob.dm(bridget, "Hey there, Bridget :)")
Direct message from [u'udp4', [u'127.0.0.1', 3939], u'bob']
u'Hey there, Bridget :)'

### Track 1 Ops

>>> helloname = gbob.mkname(bob, "hello")
>>> hellobob  = gbob.document(helloname)
>>> hellobrg  = gbrg.document(helloname)
>>> hwbob = hellobob.content
>>> hwbrg = hellobrg.content

>>> gbob.add_participant(helloname, bridget)
>>> invite = gbrg.validate_pop()
>>> print str(invite)
A user invited you to join a document and load a copy from them. author: [u'udp4', [u'127.0.0.1', 3939], u'bob'], docname: u'["udp4",["127.0.0.1",3939],"bob"]\\x00hello'
>>> invite.approve()

>>> hwbob["goofy"] = "gorsh"

>>> hwbrg
w<{u'goofy': 'gorsh'}>
>>> gbrg.can_read(bridget, helloname)
True
>>> hwbrg["Blabarsylt"] = "Swedish jelly"
>>> hwbrg["Blabarsylt"] = "Made of blueberries"

>>> hwbob["Blabarsylt"]
w<'Made of blueberries'>
>>> hellobob.routes_to(bob)
[[u'udp4', [u'127.0.0.1', 3940], u'bridget']]

### RSA

# Will do later
'''
