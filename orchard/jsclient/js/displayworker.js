// displayworker.js :: The internal worker used by display.js

// dependencies: loads util and ctree automatically

log = function(obj) {postMessage(['log',obj])}

var window = {}
importScripts('/js/util.js');
serial = window.serial;
importScripts('/js/operation.js','/js/ctree.js');

CTree = window.CTree
cursors = {0:0};
locked = false;
tree = new CTree("") // The document for this display

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
    op = new window.Operation(op.instructions);
    op.apply(tree);
    rewrite();
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
