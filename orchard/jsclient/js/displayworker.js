// displayworker.js :: The internal worker used by display.js

// dependencies: loads util and ctree automatically

log = function(obj) {postMessage(['log',obj])}

importScripts('/js/util.js');
importScripts('/js/operation.js','/js/ctree.js');

CTree = this.CTree
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

    op = new Operation([]);
    op.pushflatinsert(pos, value, tree);
    tree.apply(op);

    rewrite();
    pushCursors();
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
    op = new this.Operation(op.instructions);
    op.apply(tree);
    rewrite();
}

function lock() {
    locked = true;
    postMessage(["lock"]);
}

function unlock() {
    locked = true;
    postMessage(["unlock"]);
}

onmessage = function(e){
    data = e.data;
    log("Receiving: "+JSON.stringify(data));
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
        lock(); break;
      case "unlock":
        unlock(); break;
      default:
        return log("Unknown message type:"+type.toString());
    }
}
