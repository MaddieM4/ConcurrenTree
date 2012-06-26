__all__ = [
	'engine',
	'gear',
	'host_table',
]

__doc__ = '''

A demo of how to use the MCP system, as well as a unit test.
Note that this is a sorta silly demo since both gears/clients
are running in the same process and the same MCP router.

### Setting up communication

>>> from sys import stderr
>>> from ConcurrenTree.model.mcp import engine
>>> from ConcurrenTree.model.document import mkname

>>> localip = '127.0.0.1'
>>> bob = ['udp4', [localip, 3939], "bob"]
>>> bridget = ['udp4', [localip, 3940], "bridget"]

>>> e = engine.Engine()
>>> gbob = e.make('bob','', bob, ["rotate", 3])
>>> gbrg = e.make('bridget','', bridget, ["rotate", 7])
>>> gbob.hosts.wrapper
w<{'content': {'["udp4",["127.0.0.1",3939],"bob"]': {'encryptor': [['rotate', 3], []]}}, 'routing': {}}>
>>> gbrg.hosts.wrapper
w<{'content': {'["udp4",["127.0.0.1",3940],"bridget"]': {'encryptor': [['rotate', 7], []]}}, 'routing': {}}>

>>> gbrg.client #doctest: +ELLIPSIS
<ejtp.client.Client object at 0x...>
>>> gbob.client #doctest: +ELLIPSIS
<ejtp.client.Client object at 0x...>

>>> gbrg.hosts.crypto_set(bob, ["rotate", 3])
>>> gbrg.hosts.crypto_get(bob)
['rotate', 3]
>>> gbrg.hosts.crypto_get(bridget)
['rotate', 7]
>>> gbrg.client.encryptor_cache == gbrg.client_cache
True
>>> type(gbrg.client.encryptor_cache)
<class 'ConcurrenTree.model.mcp.gear.ClientCache'>
>>> gbrg.writer.hello(bob)

>>> hello_request = gbob.gv.pop()
>>> hello_request #doctest: +ELLIPSIS
<ConcurrenTree.model.validation.hello.HelloRequest object at ...>
>>> hello_request.approve()

>>> gbob.hosts.crypto_get(bridget)
['rotate', 7]

### Track 1 Ops

>>> helloname = mkname(bob, "hello")
>>> hellobob  = gbob.document(helloname)
>>> hellobrg  = gbrg.document(helloname)
>>> hwbob = hellobob.content
>>> hwbrg = hellobrg.content

>>> gbob.owns(helloname)
True
>>> gbob.add_participant(helloname, bridget)
>>> gbob.send_full(helloname, [bridget])

>>> hwbob["goofy"] = "gorsh"

>>> hwbrg
w<{u'goofy': 'gorsh'}>
>>> gbob.can_read(bridget, helloname)
True
>>> gbrg.can_read(bridget, helloname)
True
>>> gbob.can_write(bridget, helloname)
True
>>> gbrg.can_write(bridget, helloname)
True
>>> gbrg.can_write(None, helloname)
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
