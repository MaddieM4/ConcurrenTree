# bcp.coffee :: BCP Parsing Hub

# Dependancies: CTree, Operation, Stream

class BCP
    constructor: (stream, auth) ->
        @docs = []
        @stream = stream
        @stream.onmessage = @recieve
        @auth = auth
        @selected = ""
        @subscriptions = {}
        @bflag = {}
        @other = 
            selected: ""
            subscriptions: {}
        @getcached = {}
    recieve: (message) =>
        message = message[..-2] # get rid of nullbyte
        @log "recieving", message
        console.log "Incoming message: #{message}"
        try
            msg = JSON.parse message
        catch error
            @log?("error","bad message from remote end")
            # probably bad json
        @handle msg
        return
    local: (op, name) ->
        ###
        Process a locally-generated op
        ###
        console.log "selecting"
        @select name
        console.log "sending local"
        @docssend name, op
        console.log "sending proto"
        @send op.proto()
    select: (name) ->
        assert typeof name is "string", "Docnames must be a string"
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
        assert typeof name is "string", "Docnames must be a string"
        
        if @getcached[name] is undefined
            @getcached[name] = [[]]
            @load name
        else
            @sync name
    load: (name) ->
        @select name
        @send 
            type: "get"
            address: []
    broadcast: (name) ->
        ###
        Send a loaded document to docs as an operation, 
        or flag for it to happen when get returns
        ###
        if name is undefined then name = @selected
        assert typeof name is "string", "Docnames must be a string."
        
        if @getcached[name] is undefined
            @bflag[name] = on
        else
            op = new Operation []
            op.fromTree [], CTreeFromProto @getcached[name]
            @docssend op, name
    sync: (name) ->
        if name is undefined then name = @selected
        @select name
        @send 
            "type": "check"
            "eras": 0
    docssend: (op, name) ->
        doc.external(op, name) for doc in @docs
    register: (display) ->
        @docs.push(display)
    handle: (message) =>
        @_handle message, message.type, @handlers
    errorhandle: (message) =>
        @_handle message, message.code, @ehandlers
    _handle: (message, type, handlerset) =>
        f = handlerset[type]
        if f is undefined then f = handlerset[0]
        f @, message
    handlers: 
        "hashvalue": (self, message) ->
            md5table[message.value] = message.hashvalue
        "error": (self, message) ->
            self.errorhandle message
        "tree": (self, message) ->
            self.getcached[message.docname] = message.tree
            if self.bflag[message.docname]
                self.broadcast message.docname
                self.bflag[message.docname] = off
        0: (self, message) ->
            console.log "error: unknown message type"
            self.error 401
    ehandlers: 
        100: (self, message) ->
            self.log "connection", "broken"
            console.error "Connection broken"
        101: (self, message) ->
            self.log "connection", "started"
        0: (self, message) ->
            m = JSON.stringify message
            self.log "server error", m
            console.error "Server error: #{m}"
    send: (obj) ->
        s = JSON.stringify obj
        @log "sending", s
        @stream.send s
    error: (code) ->
        @send
            "type": "error"
            "code": code
    log: (headline, detail) ->
    reconnect: ->
        @stream.reconnect()

window.BCP = BCP
