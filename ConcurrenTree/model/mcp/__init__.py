__all__ = [
	'engine',
	'gear',
]

__doc__ = '''

A demo of how to use the MCP system, as well as a unit test.
Note that this is a sorta silly demo since both gears/clients
are running in the same process and the same MCP router.

### Setting up communication

>>> from sys import stderr
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
>>> gbrg.client(bridget, ["rotate", 7]).encryptor_cache == gbrg.client_cache
True
>>> type(gbrg.client(bridget, ["rotate", 7]).encryptor_cache)
<class 'ConcurrenTree.model.mcp.gear.ClientCache'>
>>> gbrg.hello(bob)

>>> hello_request = gbob.validate_pop()
>>> hello_request #doctest: +ELLIPSIS
<ConcurrenTree.model.validation.hello.HelloRequest object at ...>
>>> hello_request.approve()

>>> gbob.resolve(bridget)
['rotate', 7]

### Track 1 Ops

>>> helloname = gbob.mkname(bob, "hello")
>>> hellobob  = gbob.document(helloname)
>>> hellobrg  = gbrg.document(helloname)
>>> hwbob = hellobob.content
>>> hwbrg = hellobrg.content

>>> gbob.add_participant(helloname, bridget)
>>> gbob.send_full(helloname, [bridget])

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
