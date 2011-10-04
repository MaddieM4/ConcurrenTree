# ctree.coffee :: CTree object and DocumentHandler object

# Dependencies: Util

window = this;

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

    flatten: ->
        result = ""
        for p in [0..@length]
          nodes = @kids(p)
          result += node.flatten() for node in nodes
          result += @value[p] if p<@length
        result

    get: (pos, key) ->
        @children[pos][key]

    keys: (pos) ->
        #sorted keys at this position
        (key for key of @children[pos]).sort()

    kids: (pos) ->
        #sorted children at this position
        @get(pos,key) for key in @keys(pos)

    jump: (pos, key) ->
        key if pos is @length
        else [pos, key]

protostr = (item) ->
    i if typeof i is "string"
    else ""

protoval = (list) ->
    (protostr(i) for i in list).join("")

this.CTreeFromProto = (proto)->
    deletions = proto.pop()
    value = protoval(proto)
    tree = new CTree(value)
    tree.deletions = deletions
    for i in proto
      tree.insert_obj window.CTreeFromProto i if typeof i is not "string"
    tree

this.CTree = CTree
