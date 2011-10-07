# display.coffee :: A WebWorkers-based user IO class.

# dependencies: util and ctree are loaded automatically by worker

context = window

workerurl = "/js/displayworker.js"

class Display
    constructor: (@docname, @handler, @immediate) ->
        @islocked = off
        @switching = off
        @ready = off
        @worker = new Worker workerurl
        @worker.onconnect = @onwconnect
        @worker.onmessage = @onwmessage
        @worker.onerror   = @onwerror
        @onwrite = null
        @ondelete = null
        @onmove = null
        @onrewrite = null
        @onlock = null
        @onunlock = null
        @handler.register @

    external: (op, name) ->
        @apply op if (name is @docname)

    internal: (op) ->
        @handler.local op, @docname

    apply: (op) ->
        @worker.postMessage(["op", op])

    lock: (callback) ->
        throw "Display in switching state, cannot lock" if @switching
        @switching = on
        @onlock = callback if callback?
        @worker.postMessage(["lock"])

    unlock: (callback) ->
        throw "Display in switching state, cannot unlock" if @switching
        @switching = on
        @onunlock = callback if callback?
        @worker.postMessage(["unlock"])

    act: (callback) =>
        newcallback = =>
          callback(this)
          this.unlock()
        this.lock newcallback

    cursor: (id, pos) ->
        @checklock()
        @worker.postMessage ["cursor", id, pos]

    insert: (value) ->
        @checklock()
        @worker.postMessage ["insert", value]

    delete: (amount) ->
        @checklock()
        @worker.postMessage ["delete", amount]

    checklock: ->
        throw "Display not locked or in switching state" if !@islocked or @switching

    onwconnect: (e) =>
        @ready = on

    onwmessage: (e) =>
        data = e.data
        console.log("Display worker output: "+JSON.stringify(data))
        type = data[0]
        switch type
          when "op"  then @internal new Operation data[1].instructions
          when "log" then console.log data[1]
          when "lock" then @_onlock()
          when "unlock" then @_onunlock()
          when "cursor","rewrite","write","delete" then @event data

    onwerror: (e) =>
        console.error(e)
        @ready = off

    event: (message) ->
        switch message[0]
          when "cursor" then @onmove?(message[1])
          when "write" then @onwrite(message[1], message[2])
          when "delete" then @ondelete?(message[1], message[2])
          when "rewrite" then @onrewrite?(message[1])
          when "lock" then @_onlock()
          when "unlock" then @_onunlock()

    _onlock: ->
        @switching = off
        @islocked = on
        @onlock?()

    _onunlock: ->
        @switching = off
        @islocked = off
        @onunlock?()

    close: ->
        @worker.postMessage(["close"])

context.Display = Display
