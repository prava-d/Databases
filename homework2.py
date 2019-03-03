######################################################################
#
# HOMEWORK 2
#
# Due: Sun 3/3/19 23h59.
#
# Name:
#
# Email:
#
# Remarks, if any:
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



class Relation:

    def __init__ (self, columns, primary_key, tuples=[]):

        self._columns = columns
        self._primary_key = primary_key
        self._tuples = set(tuples)

    def __repr__ (self):

        result = "------------------------------------------------------------\n"
        result += (", ".join(self._columns)) + "\n"
        result += "------------------------------------------------------------\n"
        result += "".join([ str(t)+"\n" for t in self._tuples ])
        result += "------------------------------------------------------------"
        return result

    def columns (self):

        return self._columns

    def primary_key (self):

        return self._primary_key

    def tuples (self):

        return self._tuples


    ########################################
    # LOW-LEVEL CRUD OPERATIONS
    ########################################

    def create_tuple (self,tup):

        for pkey in self._primary_key:
          for onetup in self._tuples:
            if tup[self._columns.index(pkey)] == onetup[self._columns.index(pkey)]:
              raise Exception ('The input tuple conflicts with an existing primary key.')

        if len(self._columns) != len(tup):
          raise Exception ('The input tuple is not of the right size.')
        else:
          self._tuples.add(tup)


    def read_tuple (self,pkey):

        flag = 0

        for onetup in self._tuples:
          if set(pkey).issubset(onetup):
            flag = 1
            rettup = onetup

        if not flag:
          raise Exception ('The tuple with those primary keys does not exist.')

        return rettup


    def delete_tuple (self,pkey):

        flag = 0

        for onetup in self._tuples:
          if set(pkey).issubset(onetup):
            flag = 1
            deltup = onetup

        if not flag:
          raise Exception ('The tuple with those primary keys does not exist.')
        else:
          self._tuples.remove(deltup)



    ########################################
    # RELATIONAL ALGEBRA OPERATIONS
    ########################################

    def project (self,names):

        indicies = []
        primaryKeyExists = True
        for name in names:
                if name not in self._primary_key:
                    primaryKeyExists = False
                if name not in self._columns:
                    raise Exception ('An atrribute name specified does not exist')
                else:
                    indicies.append(self._columns.index(name))
        tupleSet = set()
        for tup in self._tuples:
           newTuple = []
           for index in indicies:
               newTuple.append(tup[index])
           tupleSet.add(tuple(newTuple))

        if primaryKeyExists:
            return Relation(names,names,tupleSet)
        else:
            return Relation(names,[],tupleSet)


    def select (self,pred):

        output = set()

        for tup in self._tuples:
          dict = {}
          for i in range(len(tup)):
            dict[self._columns[i]] = tup[i]
            print(dict)
          if (pred(dict)):
                output.add(tup)

        return Relation(self._columns,self._primary_key,output)

    def union (self,rel):

        if self._columns != rel._columns:
            raise Exception ('Atrributes do not match')

        if self._primary_key != rel._primary_key:
            raise Exception ('Primary keys do not match')

        return Relation(rel._columns, rel._primary_key, (rel._tuples).union(self._tuples))

    def rename (self,rlist):
        attributes = self._columns
        pkeys = self._primary_key
        for namePair in rlist:
         if namePair[0] in attributes:
            attributes[attributes.index(namePair[0])] = namePair[1]

         if namePair[0] in pkeys:
            pkeys[pkeys.index(namePair[0])] = namePair[1]

        return(Relation(attributes,pkeys,self._tuples))

    def product (self,rel):
        notDisjoint = (any(x in self._columns for x in rel._columns))

        if notDisjoint:
                raise Exception ('Attributes are not disjoint')

        combinedAttributes = self._columns + rel._columns
        combinedpKeys = self._primary_key + rel._primary_key
        concatTuples = set()

        for tup1 in self._tuples:
            for tup2 in rel._tuples:
                concatTuples.add(tup1+tup2)

        return(Relation(combinedAttributes,combinedpKeys,concatTuples))




BOOKS = Relation(["title","year","numberPages","isbn"],
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

print(BOOKS.select(lambda t : len(t["title"]) > 20 and t["year"] > 2000))

PERSONS = Relation(["firstName", "lastName", "birthYear"],
                   ["lastName"],
                   [
                       ( "Barbara", "Tuchman", 1912 ),
                       ( "Neil", "Gaiman", 1960 ),
                       ( "Terry", "Pratchett", 1948),
                       ( "John", "Keegan", 1934),
                       ( "Jonathan", "Lethem", 1964),
                       ( "Margaret", "MacMillan", 1943),
                       ( "David", "Kertzer", 1948),
                       ( "Ted", "Chiang", 1967),
                       ( "Saunders", "Mac Lane", 1909),
                       ( "Ieke", "Moerdijk", 1958),
                       ( "Barbara", "Kingsolver", 1955)
                   ])


AUTHORED_BY = Relation(["isbn","lastName"],
                       ["isbn","lastName"],
                       [
                           ( "0345349571", "Tuchman" ),
                           ( "034538623X", "Tuchman" ),
                           ( "0393356182" , "Gaiman" ),
                           ( "0060558121" , "Gaiman" ),
                           ( "0062255655" , "Gaiman" ),
                           ( "0060853980" , "Gaiman" ),
                           ( "0060853980" , "Pratchett" ),
                           ( "0307274939" , "Keegan" ),
                           ( "0712666451" , "Keegan" ),
                           ( "1101972120" , "Chiang" ),
                           ( "0679768173" , "Kertzer" ),
                           ( "0812980660" , "MacMillan" ),
                           ( "0571205992" , "Lethem" ),
                           ( "0375724886" , "Lethem" ),
                           ( "0387977102" , "Mac Lane" ),
                           ( "0387977102" , "Moerdijk" ),
                           ( "0387984032" , "Mac Lane" ),
                           ( "0060175400" , "Kingsolver")
                       ])


def books_by_Gaiman ():

    pass


def authors_with_more_than_600_pages_books ():

    pass
