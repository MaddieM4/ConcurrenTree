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
    '''
    gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg = demo_participants()
    hwbob["goofy"] = "gorsh"
    hwbrg["Blabarsylt"] = "Swedish jelly"
    hwbrg["Blabarsylt"] = "Made of blueberries"
    return gbob, gbrg, helloname, hellobob, hellobrg, hwbob, hwbrg

### RSA

# Will do later

