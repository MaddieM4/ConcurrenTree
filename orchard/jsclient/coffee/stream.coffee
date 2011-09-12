# stream.coffee

# A Web Worker library for asynchronous IO over a channel.

types = 
    websocket: "js/stream/ws.js"

class Stream
    constructor: (@type, @url) ->
        @started = false
        @running = false

        if not @type of types
            throw "Unknown stream type"
        jsaddress = types[@type]

        @worker = new Worker jsaddress
        # Don't hook up onconnect, as it's for the worker, not the connection
        @worker.onmessage = @_message
        @worker.onerror   = @_error
        @reconnect()

    send: (value) =>
        @worker.postMessage([2, value])

    _connect: (event) =>
        @onconnect(event) if @onconnect?

    _message: (event) =>
        switch event.data[0]
            when 0 then @close()
            when 1 then @_connect(event)
            when 2 then @onmessage(event.data[1]) if @onmessage?
            else console.log("Stream worker debug: "+event.data)

    _error: (event) =>
        @onerror(event) if @onerror?

    close: =>
        @worker.postMessage [0]
        @running = false

    closed: =>
        true if started and not running

    reconnect: =>
        @close()
        @connect(@url)

    connect: (url) =>
        @worker.postMessage([1, url])
        @started = true
        @running = true

window.Stream = Stream
