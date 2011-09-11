# bcp.coffee :: BCP Parsing Hub

# Dependancies: CTree, Stream

class BCP
    constructor: (docs, stream, auth) ->
        @docs = docs
        @stream = stream
        @auth = auth
        @buffer = ""
        @selected = ""
        @subscriptions = {}
        @bflag = {}
        @other = 
            selected: ""
            subscriptions: {}
        @getcached = {}
    cycle: ->
        # read network input
        @buffer += @stream.bcp_pull()
        
        # debuffer and apply messages 
        messages = @buffer.split "\x00"
        @buffer = messages.pop()
        for m in messages
            @recieve m
        
        # update displays
        @docs.cycle()
        
        # flush the stream buffer
        @stream.onpush()
    recieve: (message) ->
        @log "recieving", message
        console.log "Incoming message: #{message}"
        try
            msg = JSON.parse message
            @handle msg
        catch error
            # probably bad json
        return
    local: (op, name) ->
        console.log "selecting"
        @select name
        console.log "sending local"
        @docs.send name, op
        console.log "sending proto"
        @send op.proto()
    select: (name) ->
        assert isString(name), "Docnames must be a string"
        if name is @selected then return
        @send 
            "type": "select"
            "docname": name
        @selected = name
    get: (name) ->
        ###
        recieve or sync a document
        does not broadcast
        ###
        if name is undefined then name = @selected
        assert isString(name), "Docnames must be a string"
        
        if @getcached[name] is undefined
            @getcached[name] = [[]]
            @load name
        else
            @sync name
    load: (name) ->
        @select name
        @send 
            type: get
            tree: 0
    broadcast: (name) ->
        ###
        Send a loaded document to docs as an operation, 
        or flag for it to happen when get returns
        ###
        if name is undefined then name = @selected
        assert isString(name), "Docnames must be a string."
        
        if @getcached[name] is undefined
            @bflag[name] = on
        else
            @docs.send name, opfromprototree @getcached[name]
    sync: (name) ->
        if name is undefined then name = @selected
        @select name
        @send 
            "type": "check"
            "eras": 0
    handle: (message) ->
        @_handle message, message.type, @handlers
    errorhandle: (message) ->
        @_handle message, message.code, @ehandlers
    _handle: (message, type, handlerset) ->
        f = handlerset[type]
        if f is undefined then f = handlerset[0]
        f message
    handlers: 
        "hashvalue": (message) ->
            md5table[message.value] = message.hashvalue
        "error": (message) ->
            @errorhandle message
        "era": (message) ->
            @getcached[message.docname] = message.tree
            if @bflag[message.docname]
                @broadcast message.docname
                @bflag[message.docname] = off
        0: (message) ->
            console.log "error: unknown message type"
            @error 401
    ehandlers: 
        100: (message) ->
            @log "connection", "broken"
            console.error "Connection broken"
        101: (message) ->
            @log "connection", "started"
        0: (message) ->
            m = JSON.stringify message
            @log "server error", m
            console.error "Server error: #{m}"
    send: (obj) ->
        s = JSON.stringify obj
        @log "sending", s
        @stream.bcp_push s + "\x00"
    error: (code) ->
        @send
            "type": "error"
            "code": code
    log: (headline, detail) ->
    reconnect: ->
        @stream.reconnect()
    thread: setInterval (->
        @cycle)
        100
        # would it not be better to use web workers? I don't know how to :)