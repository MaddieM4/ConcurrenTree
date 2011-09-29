# display.coffee :: A WebWorkers-based user IO class.

# dependencies: worker.coffee

worker = """

var window = {}
importScripts('/js/util.js');
serial = window.serial;
importScripts('js/ctree.js');
CTree = window.CTree

log = function(obj) {postMessage(['log',obj])}
cursors = {0:0};
locked = false;
tree = CTree("") // The document for this display

function pushCursors(){
    postMessage(["cursor", cursors]);
}

function rewrite(){
    postMessage(["rewrite",tree.flatten()]);
}

function insert(value){
    var pos, t, node;
    pos = cursors[0];
    t = tree.trace(pos);

    // convert to operations system later
    node = tree.resolve(t.addr);
    node.insert(t.pos, value);
    rewrite();
}

function deleteone(pos) {
    t = tree.trace(pos);

    // convert to operations system later
    node = tree.resolve(t.addr);
    node.delete(t.pos);    
}

function deletemany(amount){
    var start, times, pos;
    pos = cursors[0];
    if (amount==0) return;
    if (amount > 0) {start=pos, times=amount}
    if (amount < 0) {start=pos+amount, times=-amount}
    for (var i =0; i<times;i++){
        deleteone(start);
    }
    rewrite();
}

function operate(op) {
// work on this later
}

onmessage = function(e){
    data = e.data;
    type = data[0];
    switch(type){
      case "cursor":
        var id = data[1], value = data[2];
        cursors[id] = value;
        return postMessage(["cursor", {id:value}]);
      case "insert": return insert(data[1]);
      case "delete": return deletemany(data[1]);
      case "op": return operate(data[1]);
      case "lock":
        locked = true; break;
      case "unlock":
        locked = false; break;
      default:
        return log("Unknown message type:"+type.toString());
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
        @handler.register @

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
        throw "Display not locked or in switching state" if @islocked or @switching
        @worker.postMessage ["cursor", id, pos]

    insert: (value) ->
        throw "Display not locked or in switching state" if @islocked or @switching
        @worker.postMessage ["insert", value]

    delete: (amount) ->
        throw "Display not locked or in switching state" if @islocked or @switching
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

window.Display = Display
