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
        @insert_obj pos, child

    delete: (pos) ->
        # mark a character in this tree as deleted
        if window.isArray(pos)
          @delete x for x in [pos[0]..pos[1]]
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
          result += @value[p] if p<@length and not @deletions[p]
        result

    resolve: (addr) =>
        if addr.length is 0
          return this
        else
          if isNumber(addr[0])
            pos = addr.shift()
          else
            pos = @length
          key = addr.shift()
          child = @get(pos, key).resolve(addr)

    trace: (pos) =>
        # Returns an object with properties "address" and "pos" or throws error
        result = @_trace(pos)
        throw "CTree.trace: pos > this.flatten().length" if window.isInteger(result)
        return result

    _trace: (togo) =>
        for pos in [0..@length]
          for k in @kids(pos)
            togo = k._trace(togo)
            if not window.isNumber(togo)
              togo.address = @jump(pos, k.key).concat(togo.address)
              return togo
          return {"address":[],"pos":pos} if togo is 0
          if pos < @length and not @deletions[pos]
            togo -= 1
        togo

    get: (pos, key) ->
        throw "IndexError: CTree.get position out of range ("+pos.toString()+")" if pos > @length or pos < 0 or not window.isNumber(pos)
        throw "KeyError: CTree.get child does not exist at position "+pos+" and with key '"+key+"'" if not (@children[pos][key]? and window.isString(key))
        @children[pos][key]

    keys: (pos) ->
        #sorted keys at this position
        (key for key of @children[pos]).sort()

    kids: (pos) ->
        #sorted children at this position
        @get(pos,key) for key in @keys(pos)

    jump: (pos, key) ->
        if pos is @length
          [key]
        else [pos, key]

protostr = (item) ->
    if typeof item is "string"
      item
    else ""

protoval = (list) ->
    (protostr(i) for i in list).join("")

this.CTreeFromProto = (proto)->
    deletions = proto.pop()
    value = protoval(proto)
    tree = new CTree(value)
    tree.delete(i) for i in deletions
    pos = 0
    for i in proto
      if typeof i is "string"
        pos += i.length
      else
        tree.insert_obj pos, window.CTreeFromProto i
    tree

this.CTree = CTree
