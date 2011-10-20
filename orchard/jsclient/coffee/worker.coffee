# worker.coffee :: Module to simplify the use of Workers 

# Dependencies: BlobBuilder API, HTML5 Workers

if not window.blobworker? then window.blobworker = {}
context = window.blobworker


if not window.BlobBuilder?
    if window.WebkitBlobBuilder?
        window.BlobBuilder = window.WebKitBlobBuilder
    else if window.MozBlobBuilder?
        window.BlobBuilder = window.MozBlobBuilder
if not window.URL?
    if window.WebkitURL?
        window.URL = window.WebkitURL
    else if window.createObjectURL?
        window.URL = {
           createObjectURL: (obj) -> window.createObjectURL obj
           revokeObjectURL: (url) -> window.revokeObjectURL url
        }

context.createWorker = (obj) ->
    worker = new Worker createBlobURL obj

context.createBlob = (obj) ->
    builder = new BlobBuilder()
    builder.append obj.toString()
    builder

context.createBlobURL = (obj) ->
    getBlobURL createBlob obj

context.getBlobURL = (blob) ->
    window.URL.createObjectURL blob.getBlob()

