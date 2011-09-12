postMessage("parsing started")

var stream, queue;
stream = void 0;
queue = [];

onmessage = function(event) {
      postMessage("mainthread message("+event.data+")");
      switch (event.data[0]) {
        case 0:
          return closestream();
        case 1:
          return openstream(event.data[1]);
        default:
          return sendstream(event.data[1]);
      }
}

openstream= function(url) {
      closestream();
      postMessage("Opening stream");
      stream = new WebSocket(url);
      stream.onmessage = msg;
      stream.onconnect = con;
      stream.onerror = err;
      return postMessage([1, url]);
}

closestream = function() {
      if (stream != null) {
        postMessage("Closing stream");
        stream.close();
        return stream = void 0;
        postMessage([0])
      }
}

sendstream = function(data) {
      if (stream != null) {
        if (stream.readyState == 1) {
          clearqueue();
          return stream.send(data+"\0");
        } else queue.push(data);
      }
}

clearqueue = function() {
      if (queue.length > 0) sendstream(queue.pop())
}

cleartimer = setInterval("clearqueue()", 1000);

msg= function(event) {
      return postMessage([2, event.data]);
}

con= function(event) {
      return postMessage(1);
}

err= function(event) {
      return postMessage(event);
}

postMessage("parsing finished")
