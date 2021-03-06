######################################################################
#
# HOMEWORK 4
#
# Due: Sun 4/28/19 23h59.
#
# Name: Athmika, Chris, Prava
#
# Email: athmika@students.olin.edu
#
# Remarks, if any: Our code could be the slightest bit cleaner
# but it works (but seems to have some empty blocks)!
# Also thanks for the extension. :)
#
#
######################################################################

######################################################################
#
# Python 3 code
#
# Please fill in this file with your solutions and submit it
#
# The functions below are stubs that you should replace with your
# own implementation.
#
######################################################################
import math
class RelationUnsorted:

    def __init__ (self, columns, primary_key, tuples=[]):
        self._columns = columns
        self._primary_key = primary_key
        self._tuples = File(3)
        self._tuples.allocate_block()
        for tup in tuples:
            self.create_tuple(tup)

    def columns (self):

        return self._columns

    def primary_key (self):

        return self._primary_key

    def primary_key_of (self,t):

        indices = [ self._columns.index(c) for c in self._primary_key ]
        return tuple([ t[i] for i in indices])

    def create_tuple (self,tup):
        file = self._tuples
        numBlocks = file.size()
        block = file.pull(0)
        for i in range(0,numBlocks):
            if block.has_space():
                block.append(tup)
                file.push(i,block)
                return
            block = file.pull(i+1)
        file.allocate_block()
        block = file.pull(numBlocks)
        block.append(tup)
        file.push(numBlocks,block)

    def read_tuple (self,pkey):
        file = self._tuples
        numBlocks = file.size()
        block = file.pull(0)
        for i in range(0,numBlocks):
            for j in range(0,block.size()):
                if (block.get(j) is not None):
                    if (self.primary_key_of(block.get(j)) == pkey):
                        return block.get(j)
            block = file.pull(i+1)

        raise Exception("Not found")

    def delete_tuple (self,pkey):
        file = self._tuples
        numBlocks = file.size()
        block = file.pull(0)
        for i in range(0,numBlocks):
            for j in range(0,block.size()):
                if (block.get(j) is not None):
                    if (self.primary_key_of(block.get(j)) == pkey):
                        block.put(j,None)
                        file.push(i,block)
                        return
            block = file.pull(i+1)
        raise Exception("Not found")

    def statistics (self):

        return self._tuples.statistics()


class RelationSorted:

    def __init__ (self, columns, primary_key, tuples=[]):

        self._columns = columns
        self._primary_key = primary_key
        self._tuples = File(3)
        self._tuples.allocate_block()
        for tup in tuples:
            self.create_tuple(tup)

    def columns (self):

        return self._columns

    def primary_key (self):

        return self._primary_key

    def primary_key_of (self,t):

        indices = [ self._columns.index(c) for c in self._primary_key ]
        return tuple([ t[i] for i in indices])

    def binary_search(self,file,key,start,end):
        numBlocks = file.size()
        mid = int((start+end)/2)

        blockSize = file.pull(0).size()
        blockToPull = math.ceil(mid/blockSize)-1
        if (mid%blockSize) == 0:
            tupleToGet = blockSize-1
        else:
            tupleToGet = (mid%blockSize)-1

        if mid < blockSize:
            tupleToGet = mid - 1
            blockToPull = 0

        if(start > mid):
             return 0,0,0,file.pull(0)
        elif( mid > end):
            block =  file.pull(numBlocks-1)
            tuple = block.get(self.myLast(block))
            midPrimary = self.primary_key_of(tuple)
            if key < midPrimary:
                return end,(blockToPull),(tupleToGet+1),file.pull(numBlocks-1)
            else:
                return end,(blockToPull),None,file.pull(numBlocks-1)

        if (blockToPull >= numBlocks):
            return end,(blockToPull),None,file.pull(numBlocks-1)

        block =  file.pull(blockToPull)
        tuple = block.get(tupleToGet)
        midPrimary = self.primary_key_of(tuple)

        if (tupleToGet+1) >= blockSize:
                if (blockToPull+1 >= numBlocks):
                    nextTuple = None
                else:
                    nextBlock = file.pull(blockToPull+1)
                    nextTuple = nextBlock.get(0)
        else:
            nextTuple = block.get(tupleToGet+1)

        if (nextTuple is None):
            if key > midPrimary:
                return end,(blockToPull),None,file.pull(numBlocks-1)
            else:
                return end,(blockToPull),(tupleToGet),file.pull(numBlocks-1)

        nextPrimary = self.primary_key_of(nextTuple)
        if (midPrimary < key) and (nextPrimary > key):
            return mid,blockToPull,(tupleToGet+1),block
        elif midPrimary < key:
            return self.binary_search(file,key,mid+1,end)
        elif midPrimary > key:
            return self.binary_search(file,key,start,mid-1)

    def read_binary_search(self,file,key,start,end):
        numBlocks = file.size()
        mid = int((start+end)/2)

        blockSize = file.pull(0).size()
        blockToPull = math.ceil(mid/blockSize)-1
        if (mid%blockSize) == 0:
            tupleToGet = blockSize-1
        else:
            tupleToGet = (mid%blockSize)-1

        if mid < blockSize:
            tupleToGet = mid - 1
            blockToPull = 0

        if(start > mid or mid > end):
            raise Exception("NOT FOUND")

        if (blockToPull >= numBlocks):
            raise Exception("NOT FOUND")

        block =  file.pull(blockToPull)
        tuple = block.get(tupleToGet)
        midPrimary = self.primary_key_of(tuple)

        if (midPrimary == key):
            return tuple
        elif midPrimary < key:
            return self.read_binary_search(file,key,mid+1,end)
        elif midPrimary > key:
            return self.read_binary_search(file,key,start,mid-1)

    def del_binary_search(self,file,key,start,end):
        numBlocks = file.size()
        mid = int((start+end)/2)
        print(start,mid,end)

        blockSize = file.pull(0).size()
        blockToPull = math.ceil(mid/blockSize)-1

        if (mid%blockSize) == 0:
            tupleToGet = blockSize-1
        else:
            tupleToGet = (mid%blockSize)-1

        if mid < blockSize:
            tupleToGet = mid - 1
            blockToPull = 0

        if(start > mid or mid > end):
            raise Exception("NOT FOUND")

        if (blockToPull >= numBlocks):
            raise Exception("NOT FOUND")

        block =  file.pull(blockToPull)
        tuple = block.get(tupleToGet)
        midPrimary = self.primary_key_of(tuple)
        if (midPrimary == key):
            return mid,tupleToGet,blockToPull
        elif midPrimary < key:
            return self.del_binary_search(file,key,mid+1,end)
        elif midPrimary > key:
            return self.del_binary_search(file,key,start,mid-1)


    def myLast(self,block):
        blockSize = block.size()

        i = 0
        while (block.get(i) is not None):
            i = i + 1
            if (i >= blockSize):
                return i-1
        return i-1

    def create_tuple (self,tup):

        file = self._tuples
        numBlocks = file.size()
        key = self.primary_key_of(tup)

        block =  file.pull(numBlocks-1)
        blockSize = block.size()
        last =  self.myLast(block)

        if (last == -1 and numBlocks == 1):
            block.append(tup)
            file.push(0,block)
            return

        end = (blockSize*(numBlocks-1)) + last + 1
        mid,midblockIndex,tupleIndex,block = self.binary_search(file,key,1,end)
        if tupleIndex is None:
            if (self.myLast(block)+1>=blockSize):
                file.allocate_block()
                block = file.pull(numBlocks)
                block.put(0,tup)
                file.push(numBlocks,block)
                return
            block = file.pull(numBlocks-1)
            block.put(self.myLast(block)+1,tup)
            file.push(numBlocks-1,block)
            return



        numElementsToShift = end - (mid-1)
        numShifted = 0
        prev = tup
        i = midblockIndex


        while(numShifted <= numElementsToShift):
            if tupleIndex >= blockSize:
                i = i+1
                if (i>=numBlocks):
                    file.allocate_block()
                block = file.pull(i)
                tupleIndex = 0
                temp = prev
                prev = block.get(tupleIndex)
                block.put(tupleIndex,temp)
                file.push(i,block)
                numShifted = numShifted + 1
                tupleIndex = tupleIndex + 1
            else:
                temp = prev
                prev = block.get(tupleIndex)
                block.put(tupleIndex,temp)
                file.push(i,block)
                numShifted = numShifted + 1
                tupleIndex = tupleIndex + 1


    def read_tuple (self,pkey):
        file = self._tuples
        numBlocks = file.size()
        block =  file.pull(numBlocks-1)
        blockSize = block.size()
        last =  self.myLast(block)

        end = (blockSize*(numBlocks-1)) + last + 1

        return self.read_binary_search(file,pkey,1,end)

    def delete_tuple (self,pkey):

        file = self._tuples
        numBlocks = file.size()
        block =  file.pull(numBlocks-1)
        blockSize = block.size()
        last =  self.myLast(block)

        end = (blockSize*(numBlocks-1)) + last + 1

        mid,tupleIndex,blockIndex = self.del_binary_search(file,pkey,1,end)
        if (tupleIndex == blockSize-1 and blockIndex == numBlocks-1):
            block = file.pull(numBlocks-1)
            block.put(blockSize-1,None)
            file.push(numBlocks-1,block)

        block = file.pull(blockIndex)
        numElementsToShift = end - (mid-1)
        numShifted = 1
        next = block.get(tupleIndex+1)
        i = blockIndex

        while(numShifted <= numElementsToShift):
                if (tupleIndex+1) >= blockSize and i+1 < numBlocks:
                    i = i + 1
                    nextBlock = file.pull(i)
                    tupleIndex = 0
                    next = nextBlock.get(tupleIndex)
                    block.put(blockSize-1,next)
                    file.push(i-1,block)
                    block = nextBlock
                else:
                    next = block.get(tupleIndex+1)
                    block.put(tupleIndex,next)
                    file.push(i,block)
                    tupleIndex = tupleIndex + 1

                numShifted = numShifted + 1


    def statistics (self):

        return self._tuples.statistics()


class RelationIndexed:

    def __init__ (self, columns, primary_key, tuples=[]):

        self._columns = columns
        self._primary_key = primary_key
        self._tuples = File(3)
        self._tuples.allocate_block()   # for the index
        self._tuples.allocate_block()   # content starts here
        for tup in tuples:
            self.create_tuple(tup)

    def columns (self):

        return self._columns

    def primary_key (self):

        return self._primary_key

    def primary_key_of (self,t):

        indices = [self._columns.index(c) for c in self._primary_key]
        return tuple([ t[i] for i in indices])

    def delete(self,blockIndex,insPos):

        file = self._tuples
        numBlocks = file.size()-1 #num blocks with tuples
        tupleIndex = insPos
        block =  file.pull(numBlocks-1)
        blockSize = block.size()
        last =  self.myLast(block)

        insPos = blockSize*(blockIndex-1) + insPos + 1
        end = (blockSize*(numBlocks-1)) + last - 1

        block = file.pull(blockIndex)
        numElementsToShift = end - (insPos-1)
        numShifted = 1
        next = block.get(tupleIndex+1)
        i = blockIndex

        while(numShifted <= numElementsToShift):
                if (tupleIndex+1) >= blockSize and i+1 < numBlocks:
                    i = i + 1
                    nextBlock = file.pull(i)
                    tupleIndex = 0
                    next = nextBlock.get(tupleIndex)
                    block.put(blockSize-1,next)
                    file.push(i-1,block)
                    block = nextBlock
                else:
                    next = block.get(tupleIndex+1)
                    block.put(tupleIndex,next)
                    file.push(i,block)
                    tupleIndex = tupleIndex + 1

                numShifted = numShifted + 1

        self.delupdateIndex(file,file.pull(0))
        return

    def myLast(self,block):
        blockSize = block.size()

        i = 0
        while (block.get(i) is not None):
            i = i + 1
            if (i >= blockSize):
                return i-1
        return i-1

    def insert(self, blockIndex, insPos, tup):

        file = self._tuples
        numBlocks = file.size()-1 #num blocks with tuples
        tupleIndex = insPos
        block =  file.pull(numBlocks-1)
        blockSize = block.size()
        last =  self.myLast(block)

        insPos = blockSize*(blockIndex-1) + insPos + 1
        end = (blockSize*(numBlocks-1)) + last - 1
        numElementsToShift = end - (insPos)
        numShifted = 0
        prev = tup
        i = blockIndex
        block =  file.pull(blockIndex)
        while(numShifted <= numElementsToShift):
            if tupleIndex >= blockSize:
                i = i+1
                if (i>=numBlocks):
                    file.allocate_block()
                block = file.pull(i)
                tupleIndex = 0
                temp = prev
                prev = block.get(tupleIndex)
                block.put(tupleIndex,temp)
                file.push(i,block)
                numShifted = numShifted + 1
                tupleIndex = tupleIndex + 1
            else:
                temp = prev
                prev = block.get(tupleIndex)
                block.put(tupleIndex,temp)
                file.push(i,block)
                numShifted = numShifted + 1
                tupleIndex = tupleIndex + 1

    def findPosInTuple(self,block,key):
        filledBlockSize = self.myLast(block)
        i = 0
        while (self.primary_key_of(block.get(i)) < key):
            print(block)
            i = i + 1
            if (i > filledBlockSize):
                return i
        return i

    def updateIndex(self,file,firstBlock):
        #update index
        newListWithIndices = [] #length of tuple with indices
        numBlocks = file.size()

        for i in range(1,numBlocks):
            if (i==1): fkey = self.primary_key_of(file.pull(1).get(0))
            if file.pull(i).get(0) is not None:
                temp_p_key = self.primary_key_of(file.pull(i).get(0))
                newListWithIndices.append(temp_p_key)


        firstBlock.put(0,tuple(newListWithIndices))
        file.push(0,firstBlock)
        return

    def delupdateIndex(self,file,firstBlock):
            #update index
            newListWithIndices = [] #length of tuple with indices
            numBlocks = file.size()

            if (self.myLast(file.pull(1)) == 0):
                firstBlock.put(0,tuple(newListWithIndices))
                file.push(0,firstBlock)
                return

            for i in range(1,len(firstBlock.get(0))+1):
                if (i==1): fkey = self.primary_key_of(file.pull(1).get(0))
                if file.pull(i).get(0) is not None:
                    temp_p_key = self.primary_key_of(file.pull(i).get(0))
                    newListWithIndices.append(temp_p_key)

            firstBlock.put(0,tuple(newListWithIndices))
            file.push(0,firstBlock)

    def create_tuple (self,tup):

        file = self._tuples
        firstBlock = file.pull(0)
        blockSize = firstBlock.size()
        tupleWithIndices = firstBlock.get(0)
        pkey = self.primary_key_of(tup)

        #If there is no tuple in the first block, create a tuple and insert it to the block
        if tupleWithIndices is None:
            tupleWithIndices = (pkey,)
            firstBlock.put(0,tupleWithIndices)
            file.allocate_block()
            secondBlock = file.pull(1)
            secondBlock.put(0,tup)
            file.push(0,firstBlock)
            file.push(1,secondBlock)
            return

        idx = 0 #tuple index
        blockidx = 1 #block index
        finalblockidx = 0

        primaryKeyInIndex = tupleWithIndices[idx]
        print(pkey)

        while(primaryKeyInIndex < pkey):
            idx = idx + 1
            blockidx = blockidx + 1

            if idx >= len(tupleWithIndices):
                #The tuple has to be inserted at the last block
                blockidx =  blockidx -1
                block = file.pull(blockidx)
                if block.has_space():
                    insPos = self.findPosInTuple(block,pkey)
                    self.insert(blockidx,insPos,tup)
                else:
                    file.allocate_block()
                    blockSize += 1
                    block = file.pull(blockidx+1)
                    file.push(blockidx+1, block)
                self.updateIndex(file,firstBlock)
                return

            primaryKeyInIndex = tupleWithIndices[idx]

        if (primaryKeyInIndex == pkey):
            raise Exception ("Tuple with primary key already exists")
            return

        finalblockidx = blockidx - 1
        if (finalblockidx < 1):
            finalblockidx = blockidx
            self.insert(blockidx,0,tup)
        else:
            prevBlock = file.pull(finalblockidx)
            prevlasttup = prevBlock.get(prevBlock.size() - 1)
            prevlastpkey = self.primary_key_of(prevlasttup)

            if (prevlastpkey < pkey):
                finalblockidx = blockidx

            block = file.pull(finalblockidx)
            insPos = self.findPosInTuple(block,pkey)
            self.insert(finalblockidx,insPos,tup)

        self.updateIndex(file,firstBlock)
        return

    def read_tuple (self,pkey):
        file = self._tuples
        indexBlock = file.pull(0)
        tuplesWithIndices = indexBlock.get(0)

        idx = 1
        for i in range(0, len(tuplesWithIndices)):
            if (tuplesWithIndices[i] > pkey) or (len(tuplesWithIndices) == 1): #if the elemet we are on is == to pkey
                if i == 0:
                    idx = i + 1
                    break
                else:
                    idx = i
                    break
            if (i == len(tuplesWithIndices)-1):
                    idx = i + 1
                    break

        readBlock = file.pull(idx)
        for i in range(0, readBlock.size()):
            readtuple = readBlock.get(i)
            if self.primary_key_of(readtuple) == pkey:
                return readtuple

        raise Exception("The data corresponding to that primary key does not exist")


    def delete_tuple (self,pkey):

        file = self._tuples
        firstBlock = file.pull(0)
        tuplesWithIndices = firstBlock.get(0)

        if tuplesWithIndices is None:
            raise Exception("The file is empty")

        if (len(tuplesWithIndices) == 1 and self.myLast(file.pull(1))==0):
            block = file.pull(1)
            block.put(0,None)
            file.push(1, block)
            self.delupdateIndex(file,file.pull(0))
            return

        blockidx = 1

        for i in range(0, len(tuplesWithIndices)):
            if (tuplesWithIndices[i] > pkey):
                if i == 0 or (len(tuplesWithIndices) == 1):
                    blockidx = i + 1
                else:
                    blockidx = i
                break
            if (i == len(tuplesWithIndices) - 1):
                blockidx = i + 1
                break

        deleteBlock = file.pull(blockidx)

        deleteidx = 0
        foundflag = 0
        flag = 0
        for i in range(0, self.myLast(deleteBlock) + 1):
            print("START", i)
            tup = deleteBlock.get(i)
            thispkey = self.primary_key_of(tup)
            if (thispkey == pkey):
                deleteidx = i
                foundflag = 1
                break

        if not foundflag:
            raise Exception("The data corresponding to that primary key does not exist")

        self.delete(blockidx,deleteidx)
        return

    def statistics (self):

        return self._tuples.statistics()

############################################################
# API to files and blocks
#
# A file is basically an array of blocks
# You have to pull and push blocks explicitly to work on them
# and commit your changes
#
# A block is basically an array of tuples
#
# I know this code looks weird, really weird. That's because
# I really wanted to hide the underlying implementation as an
# array so that you're forced to use the API I provide. Python
# makes it ridiculously difficult to enforce this kind of thing
# (something that would be _private_ in a different language).
#
# The code below relies on an underlying implementation in terms of
# FileImplementation and BlockImplementation, where the implementation
# objects are hidden in the local environment of a closure. If this
# is mysterious, find a copy of "Structure and Interpretation of
# Computer Programs" and read chapter 3.
#

class File:

    def __init__ (self,block_size):

        self._impl = (lambda obj : { "__repr__": (lambda : FileImplementation.__repr__(obj)),
                                     "size": (lambda : FileImplementation.size(obj)),
                                     "allocate_block": (lambda : FileImplementation.allocate_block(obj)),
                                     "pull": (lambda i : FileImplementation.pull(obj,i)),
                                     "push": (lambda i,block : FileImplementation.push(obj,i,block)),
                                     "statistics": (lambda : FileImplementation.statistics(obj)) })(FileImplementation(block_size))

    def __repr__ (self):

        return self._impl["__repr__"]()

    def size (self):

        return self._impl["size"]()

    def allocate_block (self):

        return self._impl["allocate_block"]()

    def pull (self,i):

        return self._impl["pull"](i)

    def push (self,i,block):

        return self._impl["push"](i,block)

    def statistics (self):

        return self._impl["statistics"]()


class Block:

    def __init__ (self,size):

        self._impl = (lambda obj : { "__repr__": (lambda : BlockImplementation.__repr__(obj)),
                                     "has_space": (lambda : BlockImplementation.has_space(obj)),
                                     "size": (lambda : BlockImplementation.size(obj)),
                                     "last": (lambda : BlockImplementation.last(obj)),
                                     "append": (lambda tup : BlockImplementation.append(obj,tup)),
                                     "get": (lambda i : BlockImplementation.get(obj,i)),
                                     "put": (lambda i,tup : BlockImplementation.put(obj,i,tup)),
                                     "clone": (lambda : BlockImplementation.clone(obj)) })(BlockImplementation(size))

    def __repr__ (self):

        return self._impl["__repr__"]()

    def has_space (self):

        return self._impl["has_space"]()

    def size (self):

        return self._impl["size"]()

    def last (self):

        return self._impl["last"]()

    def append (self,tup):

        return self._impl["append"](tup)

    def get (self,i):

        return self._impl["get"](i)

    def put (self,i,tup):

        return self._impl["put"](i,tup)

    def clone (self):

        return self._impl["clone"]()




############################################################
# Implementation of blocks and files
#

class FileImplementation:

    def __init__ (self,block_size):

        self._content = []
        self._size = 0
        self._read = 0
        self._write = 0
        self._block_size = block_size

    def __repr__ (self):

        fmt = "------------------------------------------------------------\n{}\n"
        return "".join([ fmt.format(x) if x else "-" for x in self._content ])

    def size (self):

        return self._size

    def allocate_block (self):

        self._size += 1
        self._content.append(Block(self._block_size))

    def pull (self,i):

        if i in range(self._size):
            self._read += 1
            print("[ reading block @ {}: {} ]".format(i,self._content[i]))
            return self._content[i].clone()

    def push (self,i,block):

        if i in range(self._size):
            self._write += 1
            print("[ writing block @ {}: {} ]".format(i,block))
            self._content[i] = block

    def statistics (self):

        return (self._read,self._write)


class BlockImplementation:

    def __init__ (self, size):

        self._size = size;
        self._available = 0;
        self._content = [ None for _ in range(size) ]

    def __repr__ (self):

        return " ".join([ str(x) if x else "-" for x in self._content ])

    def has_space (self):

        return self._available < self._size

    def size (self):

        return self._size

    def last (self):

        return self._available-1

    def append (self,tup):

        if self.has_space():
            self.put(self._available,tup)
            self._available += 1
        else:
            raise Exception("Problem!")

    def get (self,i):

        if i in range(self._size):
            return self._content[i]

    def put (self,i,tup):

        if i in range(self._size):
            self._content[i] = tup

    def clone (self):

        copy = Block(self._size)
        for i in range(0,self._available):
            copy.append(self.get(i))
        for i in range(self._available,self._size):
            copy.put(i,self.get(i))
        return copy


# Uncomment as appropriate to have some testing relations
'''
 BOOKS = RelationUnsorted(["title","year","numberPages","isbn"],
                          ["isbn"],
                          [
                              ( "A Distant Mirror", 1972, 677, "0345349571"),
                              ( "The Guns of August", 1962, 511, "034538623X"),
                              ( "Norse Mythology", 2017, 299, "0393356182"),
                              ( "American Gods", 2003, 591, "0060558121"),
                              ( "The Ocean at the End of the Lane", 2013, 181, "0062255655"),
                              ( "Good Omens", 1990, 432, "0060853980"),
                              ( "The American Civil War", 2009, 396, "0307274939"),
                              ( "The First World War", 1999, 500, "0712666451"),
                              ( "The Kidnapping of Edgardo Mortara", 1997, 350, "0679768173"),
                              ( "The Fortress of Solitude", 2003, 509, "0375724886"),
                              ( "The Wall of the Sky, The Wall of the Eye", 1996, 232, "0571205992"),
                              ( "Stories of Your Life and Others", 2002, 281, "1101972120"),
                              ( "The War That Ended Peace", 2014, 739, "0812980660"),
                              ( "Sheaves in Geometry and Logic", 1994, 630, "0387977102"),
                              ( "Categories for the Working Mathematician", 1978, 317, "0387984032"),
                              ( "The Poisonwood Bible", 1998, 560, "0060175400")
                          ])
'''

#books = RelationUnsorted(["title","year","numberPages","isbn"],["isbn"])

'''
print(books.read_tuple(("0060558121",)))
print(books.read_tuple(("0307274939",)))
books.delete_tuple(("0060558121",))
'''
books = RelationSorted(["title","year","numberPages","isbn"],["isbn"])

#
# books.create_tuple(( "The American Civil War", 2009, 396, "0307274939"))
# books.create_tuple(( "The Guns of August", 1962, 511, "034538623X"))
# books.create_tuple(( "Norse Mythology", 2017, 299, "0393356182"))
# books.create_tuple(( "A Distant Mirror", 1972, 677, "0345349571"))
# books.create_tuple(( "Good Omens", 1990, 432, "0060853980"))
#
# books.create_tuple(( "American Gods", 2003, 591, "0060558121"))
# books.create_tuple(( "The Ocean at the End of the Lane", 2013, 181, "0062255655"))

# print(books.read_tuple(("0393356182",)))
# print(books.read_tuple(("0345349571",)))
# print(books.read_tuple(("0060853980",)))
# print(books.read_tuple(("0393356182",)))
#print(books.read_tuple(("0307274939",)))
# print(books._tuples)
# books.delete_tuple(("034538623X",))
# books.delete_tuple(("0393356182",))
# books.delete_tuple(("0060853980",))
#books.delete_tuple(("0307274939",))
#books.delete_tuple(("0345349571",))
#books.delete_tuple(("0393356182",))
#books.delete_tuple(("0060853980",))
#books.delete_tuple(("0307274939",))
#books.delete_tuple(("0393356182",))

print(books._tuples)






'''books.create_tuple(( "A Distant Mirror", 1972, 677, "0345349571"))
books.create_tuple(( "The Guns of August", 1962, 511, "034538623X"))
books.create_tuple(( "Norse Mythology", 2017, 299, "0393356182"))
books.create_tuple(( "Good Omens", 1990, 432, "0060853980"))
books.create_tuple(( "American Gods", 2003, 591, "0060558121"))
books.create_tuple(( "The Ocean at the End of the Lane", 2013, 181, "0062255655"))
print(books.read_tuple(("0060558121",)))
print(books.read_tuple(("0307274939",)))
print(books._tuples)
books.delete_tuple(("034538623X",))
books.delete_tuple(("0393356182",))
books.delete_tuple(("0060853980",))
books.delete_tuple(("0307274939",))
#books.read_tuple(("0307books.delete_tuple(("0393356182",))'''






# BOOKS = RelationSorted(["title","year","numberPages","isbn"],
#                          ["isbn"],
#                          [
#                              ( "A Distant Mirror", 1972, 677, "0345349571"),
#                              ( "The Guns of August", 1962, 511, "034538623X"),
#                              ( "Norse Mythology", 2017, 299, "0393356182"),
#                              ( "American Gods", 2003, 591, "0060558121"),
#                              ( "The Ocean at the End of the Lane", 2013, 181, "0062255655"),
#                              ( "Good Omens", 1990, 432, "0060853980"),
#                              ( "The American Civil War", 2009, 396, "0307274939"),
#                              ( "The First World War", 1999, 500, "0712666451"),
#                              ( "The Kidnapping of Edgardo Mortara", 1997, 350, "0679768173"),
#                              ( "The Fortress of Solitude", 2003, 509, "0375724886"),
#                              ( "The Wall of the Sky, The Wall of the Eye", 1996, 232, "0571205992"),
#                              ( "Stories of Your Life and Others", 2002, 281, "1101972120"),
#                              ( "The War That Ended Peace", 2014, 739, "0812980660"),
#                              ( "Sheaves in Geometry and Logic", 1994, 630, "0387977102"),
#                              ( "Categories for the Working Mathematician", 1978, 317, "0387984032"),
#                              ( "The Poisonwood Bible", 1998, 560, "0060175400")
#                          ])

'''BOOKS = RelationIndexed(["title","year","numberPages","isbn"],
                     ["isbn"],
                     [
                         ( "A Distant Mirror", 1972, 677, "0345349571"),
                         ( "The Guns of August", 1962, 511, "034538623X"),
                         ( "Norse Mythology", 2017, 299, "0393356182"),
                         ( "American Gods", 2003, 591, "0060558121"),
                         ( "The Ocean at the End of the Lane", 2013, 181, "0062255655"),
                         ( "Good Omens", 1990, 432, "0060853980"),
                         ( "The American Civil War", 2009, 396, "0307274939"),
                         ( "The First World War", 1999, 500, "0712666451"),
                         ( "The Kidnapping of Edgardo Mortara", 1997, 350, "0679768173"),
                         ( "The Fortress of Solitude", 2003, 509, "0375724886"),
                         ( "The Wall of the Sky, The Wall of the Eye", 1996, 232, "0571205992"),
                         ( "Stories of Your Life and Others", 2002, 281, "1101972120"),
                         ( "The War That Ended Peace", 2014, 739, "0812980660"),
                         ( "Sheaves in Geometry and Logic", 1994, 630, "0387977102"),
                         ( "Categories for the Working Mathematician", 1978, 317, "0387984032"),
                         ( "The Poisonwood Bible", 1998, 560, "0060175400")])'''

#books.insert(0,0,( "A Distant Mirror", 1972, 677, "0345349571"))
#books.create_tuple(( "The American Civil War", 2009, 396, "0307274939"))
#books.create_tuple(( "A Distant Mirror", 1972, 677, "0345349571"))
#books.create_tuple(( "The Guns of August", 1962, 511, "034538623X"))
#books.create_tuple(( "Norse Mythology", 2017, 299, "0393356182"))
#print(books._tuples)
