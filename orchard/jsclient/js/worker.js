(function() {
  var createBlob, createWorker;

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
    var worker;
    return worker = new Worker(createBlobURL(obj));
  };

  createBlob = function(obj) {
    var builder;
    builder = new BlobBuilder();
    builder.append(obj.toString());
    return builder;
  };

  createBlobURL(obj)(function() {
    return getBlobURL(createBlob(obj));
  });

  getBlobURL(blob)(function() {
    return window.URL.createObjectURL(blob.getBlob());
  });

  window.blobworker = {
    createWorker: createWorker,
    createBlob: createBlob,
    createBlobURL: createBlobURL,
    getBlobURL: getBlobURL
  };

}).call(this);
