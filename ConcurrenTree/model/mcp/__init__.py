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

>>> gbob.writer.pull_index(bridget, helloname)
079eeae801303fd811fe3f443c66528a6add7e42: u'\\\\_2^[Z\\\\2Z2*/Z)*_-]+Z*\\\\2./ZZ^*.))1_Z++*)['
34004f4763524e87cfe4f5b5f915266f80bbbfe7: u'+0_].)]^Z[_1_++)Z/.,-_2*[[^00/0\\\\,*-*.)-+'
44d0cb0c7e9b77eb053294915fdb031abd98adc5: u'\\\\[../)[_,+2)/\\\\Z)Z)^0/**.Z0_[/[*^[*_]./]\\\\'
45e9f1b0334e99aac9c012b1cd1e25a2ce18c5d7: u'10)0Z.-.]+*0*\\\\.^\\\\,)//,.,_21-+[[*Z]Z2-\\\\/['
47b01407c24b8be47fe5df780f4959c01be196ae: u'^_1[,0\\\\2].*_,_Z^2+*]2*-1/0+-1Z,\\\\[[2\\\\Z+0.'
790742eb7a29172333fe025c2622ea18c5286d68: u'],-^-2,_)]2.[)/\\\\10Z\\\\\\\\-\\\\[2\\\\Z-+ZZZ21*2\\\\0.,'
9bf7b64433a119b91b8790b3697712db8ee5b090: u'*[\\\\\\\\20\\\\1[\\\\0\\\\Z.2,[0^Z.+-^0^])0Z\\\\[.*^2Z))*'
bc41162db8b81392569a5bedf52c7414212df665: u'^0**/0.^,0])\\\\_Z^0**0])^\\\\0^_0-000.2--,]\\\\_'
c5467b8ced86280298b6df359835e23bf9742ca7: u'\\\\1,2^/^[1-.1]),2^,.Z/+0,[],.\\\\^*-)1).)/*1'
d251f86d43c808ee5cbe8231ca8545419649d7c0: u']^\\\\,\\\\2.0[0^^+Z*]+0*21_1]Z2+-/2Z.^000))+.'
ed61a0b09322e3b5e0361a015c275f7e46057d52: u',Z[/.1^^.^/]^\\\\0/2221*_0\\\\Z[).^[,/_\\\\\\\\_-,[]'

### RSA

# Will do later
'''
