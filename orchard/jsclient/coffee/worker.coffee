if not BlobBuilder?
    if WebkitBlobBuilder?
        window.BlobBuilder = WebKitBlobBuilder
    else if MozBlobBuilder?
        window.BlobBuilder = MozBlobBuilder
if not window.URL?
    if window.WebkitURL?
        window.URL = window.WebkitURL
    else if window.createObjectURL?
        window.URL = {
           createObjectURL:(obj)->window.createObjectURL obj,
           revokeObjectURL:(url)->window.revokeObjectURL url
        }

createWorker=(obj) ->
    worker = new Worker createBlobURL obj

createBlob= (obj) ->
    builder = new BlobBuilder()
    builder.append obj.toString()
    builder

createBlobURL=(obj) ->
    getBlobURL createBlob obj

getBlobURL=(blob) ->
    window.URL.createObjectURL blob.getBlob()

window.blobworker = {
    createWorker,
    createBlob,
    createBlobURL,
    getBlobURL
}
