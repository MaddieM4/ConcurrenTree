if not BlobBuilder?
    if WebkitBlobBuilder?
        window.BlobBuilder = WebKitBlobBuilder
    else if MozBlobBuilder?
        window.BlobBuilder = MozBlobBuilder
if not window.URL?
    if window.WebkitURL?
        window.URL = window.WebkitURL
    
createWorker = (obj) ->
    builder = new BlobBuilder()
    builder.append obj.toString()
    worker = new Worker window.URL.createObjectURL builder.getBlob()