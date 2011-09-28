(function() {
  var createWorker;

  if (!(typeof BlobBuilder !== "undefined" && BlobBuilder !== null)) {
    if (typeof WebkitBlobBuilder !== "undefined" && WebkitBlobBuilder !== null) {
      window.BlobBuilder = WebKitBlobBuilder;
    } else if (typeof MozBlobBuilder !== "undefined" && MozBlobBuilder !== null) {
      window.BlobBuilder = MozBlobBuilder;
    }
  }

  if (!(window.URL != null)) {
    if (window.WebkitURL != null) window.URL = window.WebkitURL;
  }

  createWorker = function(obj) {
    var builder, worker;
    builder = new BlobBuilder();
    builder.append(obj.toString());
    return worker = new Worker(window.URL.createObjectURL(builder.getBlob()));
  };

}).call(this);
