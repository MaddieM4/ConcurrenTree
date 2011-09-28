# display.coffee :: A WebWorkers-based user IO class.

# dependencies: worker.coffee

worker = """

var window = {}
importScripts('js/util');
serial = window.serial;
importScripts('js/ctree.js');

log = function(obj) {postMessage(['log',obj])}
cursors = {0:0};

onmessage = function(e){
    data = e.data;
    type = data[0];
    switch(type){
      case "cursor":
        cursors[data[1]] = data[2];
        return postMessage(["cursor", {data[1]:data[2]]});
      case "insert":
        cursorpos = data[1]; return;
        return postMessage(["cursor", data[1], data[2]]);
      case "delete":
        cursorpos = data[1]; return;
        return postMessage(["cursor", data[1], data[2]]);
    }
}

"""

workerurl = blobworker.createBlobURL worker

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

    external: (op, name) ->
        @apply op if (name == @docname)

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

    cursor: (id, pos) ->
        @worker.postMessage ["cursor", id, pos]

    insert: (value) ->
        @worker.postMessage ["insert", value]

    delete: (amount) ->
        @worker.postMessage ["delete", amount]

    onwconnect: (e) ->
        @ready = on

    onwmessage: (e) ->
        data = e.data
        type = data[0]
        switch type
          when "op"  then @internal data[1]
          when "log" then console.log data[1]
          when "lock" then @_onlock()
          when "unlock" then @_onunlock()
          when "cursor","rewrite","write","delete" then @event data

    onwerror: (e) ->
        console.error(e)
        @ready = off

    event: (message) ->
        switch message[0]
          when "cursor" then @onmove?(message[1])
          when "write" then @onwrite(message[1], message[2])
          when "delete" then @ondelete?(message[1], message[2])
          when "rewrite" then @onrewrite?(message[1])

    _onlock: ->
        @switching = off
        @islocked = on
        @onlock?()

    _onunlock: ->
        @switching = off
        @islocked = off
        @onunlock?()
