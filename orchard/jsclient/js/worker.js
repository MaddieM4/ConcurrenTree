(function() {
  var context;

  if (!(window.blobworker != null)) window.blobworker = {};

  context = window.blobworker;

  if (!(window.BlobBuilder != null)) {
    if (window.WebkitBlobBuilder != null) {
      window.BlobBuilder = window.WebKitBlobBuilder;
    } else if (window.MozBlobBuilder != null) {
      window.BlobBuilder = window.MozBlobBuilder;
    }
  }

  if (!(window.URL != null)) {
    if (window.WebkitURL != null) {
      window.URL = window.WebkitURL;
    } else if (window.createObjectURL != null) {
      window.URL = {
        createObjectURL: function(obj) {
          return window.createObjectURL(obj);
        },
        revokeObjectURL: function(url) {
          return window.revokeObjectURL(url);
        }
      };
    }
  }

  context.createWorker = function(obj) {
    var worker;
    return worker = new Worker(createBlobURL(obj));
  };

  context.createBlob = function(obj) {
    var builder;
    builder = new BlobBuilder();
    builder.append(obj.toString());
    return builder;
  };

  context.createBlobURL = function(obj) {
    return getBlobURL(createBlob(obj));
  };

  context.getBlobURL = function(blob) {
    return window.URL.createObjectURL(blob.getBlob());
  };

}).call(this);
