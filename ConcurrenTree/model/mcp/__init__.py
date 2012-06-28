__all__ = [
	'engine',
	'gear',
	'host_table',
]

__doc__ = '''

A demo of how to use the MCP system, as well as a unit test.
Note that this is a sorta silly demo since both gears/clients
are running in the same process and the same MCP router.

'''

### Setting up communication

localip = '127.0.0.1'
bob = ['udp4', [localip, 3939], "bob"]
bridget = ['udp4', [localip, 3940], "bridget"]

def demo_clients():
    '''
    Create a pair of clients, bob and bridget, for testing.
    
    >>> gbob, gbrg = demo_clients()
    >>> gbob.hosts.wrapper
    w<{'content': {'["udp4",["127.0.0.1",3939],"bob"]': {'encryptor': [['rotate', 3], []]}}, 'routing': {}}>
    >>> gbrg.hosts.wrapper
    w<{'content': {'["udp4",["127.0.0.1",3940],"bridget"]': {'encryptor': [['rotate', 7], []]}}, 'routing': {}}>

    >>> gbrg.client #doctest: +ELLIPSIS
    <ejtp.client.Client object at 0x...>
    >>> gbob.client #doctest: +ELLIPSIS
    <ejtp.client.Client object at 0x...>
    '''
    from ConcurrenTree.model.mcp import engine

    e = engine.Engine()
    gbob = e.make('bob','', bob, encryptor=["rotate", 3], make_jack=False)
    gbrg = e.make('bridget','', bridget, encryptor=["rotate", 7], make_jack=False)
    return (gbob, gbrg)

def demo_clients_enc():
    '''
    Set up clients from demo_clients with encryption data.

    >>> gbob, gbrg = demo_clients_enc()
    >>> gbrg.hosts.crypto_get(bob)
    ['rotate', 3]
    >>> gbrg.hosts.crypto_get(bridget)
    ['rotate', 7]
    >>> gbrg.client.encryptor_cache == gbrg.client_cache
    True
    >>> type(gbrg.client.encryptor_cache)
    <class 'ConcurrenTree.model.mcp.gear.ClientCache'>
    '''
    gbob, gbrg = demo_clients()
    gbrg.hosts.crypto_set(bob, ["rotate", 3])
    return gbob, gbrg

def demo_clients_hello():
    '''
    Hello stage of the test.

    >>> gbob, gbrg, hello_request = demo_clients_hello()
    >>> hello_request #doctest: +ELLIPSIS
    <ConcurrenTree.model.validation.hello.HelloRequest object at ...>

    >>> gbob.hosts.crypto_get(bridget)
    ['rotate', 7]
    '''
    gbob, gbrg = demo_clients_enc()
    gbrg.writer.hello(bob)
    hello_request = gbob.gv.pop()
    hello_request.approve()
    return gbob, gbrg, hello_request


### Track 1 Ops

def demo_documents():
    '''
    From here on, a lot more variables will get passed around.

    >>> gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg = demo_documents()
    >>> gbob.owns(helloname)
    True
    '''
    from ConcurrenTree.model.document import mkname
    gbob, gbrg, _ = demo_clients_hello()
    helloname = mkname(bob, "hello")
    hellobob  = gbob.document(helloname)
    hellobrg  = gbrg.document(helloname)
    hwbob = hellobob.content
    hwbrg = hellobrg.content
    return gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg

def demo_participants():
    '''
    Add Bridget as a participant of the document.

    >>> gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg = demo_participants()
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

    >>> hellobob.routes_to(bob)
    [[u'udp4', [u'127.0.0.1', 3940], u'bridget']]
    '''
    gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg = demo_documents()
    gbob.add_participant(helloname, bridget)
    gbob.send_full(helloname, [bridget])
    return gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg

def demo_data():
    '''
    Demonstrate data transfer.
    
    >>> gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg = demo_data()
    >>> hwbrg
    w<{'Blabarsylt': 'Made of blueberries', u'goofy': 'gorsh'}>
    >>> hwbob
    w<{u'Blabarsylt': 'Made of blueberries', 'goofy': 'gorsh'}>
    
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
    
    >>> gbob.writer.pull_snapshot(bridget, helloname)
    {"content":{"Blabarsylt":"Made of blueberries","goofy":"gorsh"},"permissions":{"graph":{"edges":{},"vertices":{}},"read":{"[\\"udp4\\",[\\"127.0.0.1\\",3939],\\"bob\\"]":true,"[\\"udp4\\",[\\"127.0.0.1\\",3940],\\"bridget\\"]":true},"write":{"[\\"udp4\\",[\\"127.0.0.1\\",3939],\\"bob\\"]":true,"[\\"udp4\\",[\\"127.0.0.1\\",3940],\\"bridget\\"]":true}},"routing":{"[\\"udp4\\",[\\"127.0.0.1\\",3939],\\"bob\\"]":{},"[\\"udp4\\",[\\"127.0.0.1\\",3940],\\"bridget\\"]":{}}}
    
    >>> ophashes = [
    ...    '079eeae801303fd811fe3f443c66528a6add7e42', # Real op
    ...    'X79eeae801303fd811fe3f443c66528a6add7e42', # Real op
    ... ]
    >>> gbob.writer.pull_op(bridget, helloname, ophashes[0]) # Real op
    >>> gbob.writer.pull_op(bridget, helloname, ophashes[1]) # Fake op
    Error from: [u'udp4', [u'127.0.0.1', 3940], u'bridget'] , code 321
    u'Resource not found'
    {"id":"X79eeae801303fd811fe3f443c66528a6add7e42","res_type":"op"}
    >>> gbob.writer.pull_ops(bridget, helloname, ophashes) # Both
    Error from: [u'udp4', [u'127.0.0.1', 3940], u'bridget'] , code 321
    u'Resource not found'
    {"id":"X79eeae801303fd811fe3f443c66528a6add7e42","res_type":"op"}
    '''
    gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg = demo_participants()
    hwbob["goofy"] = "gorsh"
    hwbrg["Blabarsylt"] = "Swedish jelly"
    hwbrg["Blabarsylt"] = "Made of blueberries"
    return gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg

### RSA

# Will do later
