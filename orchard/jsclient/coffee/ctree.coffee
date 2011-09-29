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
        @insert_obj pos child

    delete: (pos) ->
        # mark a character in this tree as deleted
        @delete x for x in [pos[0]..pos[1]] if window.isArray(pos)
        else @deletions[pos] = true
        this

    insert_obj: (pos, child)->
        @children[pos][child.key] = child
        child

    get: (pos, key) ->
        @children[pos][key]

window.CTreeFromProto = (proto)->
    deletions = proto.pop()
    value = for i in proto
      i if typeof i is "string"
      else ""
    value = value.join("")
    tree = new CTree(value)
    tree.deletions = deletions
    for i in proto
      tree.insert_obj window.CTreeFromProto i if typeof i is not "string"

window.CTree = CTree
