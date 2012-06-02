__all__ = [
	'engine',
	'gear',
	'vertex',
]

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
<ejtp.client.Client object at 0x...>
>>> gbob.client(bob, ["rotate", 3]) #doctest: +ELLIPSIS
<ejtp.client.Client object at 0x...>

>>> gbrg.resolve_set(bob, ["rotate", 3])
>>> gbrg.resolve(bob)
['rotate', 3]
>>> gbrg.resolve(bridget)
['rotate', 7]
>>> gbrg.hello(bob)
>>> hello_invite = gbob.validate_pop()
>>> print str(hello_invite)
A remote interface is telling you its encryptor proto. author: [u'udp4', [u'127.0.0.1', 3940], u'bridget'], encryptor: [u'rotate', 7]
>>> hello_invite.approve()

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

>>> load_request = gbrg.validate_pop()
>>> print str(load_request)
A user requested to load a document from you. author: [u'udp4', [u'127.0.0.1', 3939], u'bob'], docname: u'["udp4",["127.0.0.1",3939],"bob"]\\x00hello'
>>> load_request.approve()

>>> invite = gbrg.validate_pop()
>>> print str(invite)
A user invited you to join a document and load a copy from them. author: [u'udp4', [u'127.0.0.1', 3939], u'bob'], docname: u'["udp4",["127.0.0.1",3939],"bob"]\\x00hello'
>>> invite.approve()

>>> load_request = gbob.validate_pop()
>>> print str(load_request)
A user requested to load a document from you. author: [u'udp4', [u'127.0.0.1', 3939], u'bob'], docname: u'["udp4",["127.0.0.1",3939],"bob"]\\x00hello'
>>> load_request.approve()

>>> hwbob["goofy"] = "gorsh"

>>> hwbrg
w<{u'goofy': 'gorsh'}>
>>> gbob.can_read(bridget, helloname)
True
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
