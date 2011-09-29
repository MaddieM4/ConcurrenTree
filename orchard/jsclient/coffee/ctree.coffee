# ctree.coffee :: CTree object and DocumentHandler object

# Dependencies: Util

class CTree
    constructor: (value) ->
        # action functions should return trees
        @value = value
        @length = value.length
        @key = serial.key value
        @deletions = []
        window.arrayFill @deletions, (-> false), @length
        @children = []
        window.arrayFill @children, (-> {}), @length+1
    insert: (pos, childtext) ->
        # insert and return a child tree
        child = new CTree childtext
        @children[pos][child.key] = child
    delete: (pos) ->
        # mark a character in this tree as deleted
        @deletions[pos] = true
        this
    get: (pos, key) ->
        @children[pos][key]

window.CTree = CTree
