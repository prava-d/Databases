######################################################################
#
# HOMEWORK 0
#
# Due: Sun 2/17/19 23h59.
# 
# Name: Prava and Athmika
# 
# Email: prava@students.olin.edu and athmika@students.olin.edu
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


class ERModel (object):

    def __init__ (self):

        self._emodel = []
        self._rmodel = []

    def entity_sets (self):

        return [i[0] for i in self._emodel]

    def create_entity_set (self,name,attributes,attributes_key):

        if name in self.entity_sets():
          raise Exception ("Duplicate set name")

        self._emodel.append([name, EntitySet(attributes,attributes_key)])

    def read_entity_set (self,name):

        if name not in self.entity_sets():
          raise Exception('The entity set by the given name does not exist.')

        for entity_set in self._emodel:
          if name == entity_set[0]:
            return entity_set[1]

    def relationship_sets (self):

        # temp = [i[1].relationship_keys() for i in self._rmodel]

        # return list((*temp))

        [list(i[1].relationship_keys() for i in self._rmodel)]

    def create_relationship_set (self,name,roles,attributes=[]):

        if name in self.relationship_sets():
        	raise Exception ('The relationship set by the given name exists.')

        self._rmodel.append([name, RelationshipSet(roles, attributes)])
    
    def read_relationship_set (self,name):

        if name not in self.relationship_sets():
        	raise Exception('The relationship set by the given name does not exist.')

        for r_set in self._rmodel:
        	if name == r_set[0]:
        		return r_set[1]


class EntitySet (object):

    def __init__ (self,attributes,attributes_key):

        self._attributes = attributes
        self._attributes_key = attributes_key
        self._entityset = []

    def entity_keys (self):
        result = []
        for entity in self._entityset:
            result.append(entity.primary_key().values()[0])

        return result

    def create_entity (self,attributes):

        for attName in attributes.keys():
          if attName in self._attributes_key:
            for entity in self._entityset:
              if attributes.get(attName) == entity.attribute(attName):
                raise Exception("Duplicate key")

        temp = Entity(attributes, self._attributes_key)
        self._entityset.append(temp)

    def read_entity (self,key):

        for entity in self._entityset:
          for entKey in entity.primary_key().values():
            if entKey == key:
              return entity

        raise Exception('There is no entity corresponding to that key.')
            
    def delete_entity (self,key):

        for i in range(len(self._entityset)):
          if _entityset[i] == key:
            del _entityset[i]
            return

        raise Exception('There is no entity corresponding to that key.')


class Entity (object):

    def __init__ (self,attributes,attributes_key):
        
        self._attributes = attributes
        self._attributes_key = attributes_key

    def __str__ (self):
        
        attrs = [ "{}={}".format(name,val) for (name,val) in self._attributes.items() ]
        return "[{}]".format("|".join(attrs))

    def attribute (self,name):
        
        return self._attributes.get(name)

    def primary_key (self):
        
        return {key: self._attributes[key] for key in self._attributes_key}


class RelationshipSet (object):

    def __init__ (self,roles,attributes):

        self._roles = roles
        self._attributes = attributes
        self._relationshipset = []
    
    def relationship_keys (self):

        return [list(i[0].values()) for i in self._relationshipset]

    def create_relationship (self,role_keys,attributes={}):

        for key, value in role_keys.items():
            if value in self.relationship_keys():
                raise Exception ('The relationship with that primary key already exists')

        self._relationshipset.append([role_keys, attributes])

    def read_relationship (self,pkey):

        for relationship in self._relationshipset:
            for key, value in relationship[0].items():
                if pkey == value:
                	return relationship

        raise Exception ('The relationship with that primary key does not exist')


    def delete_relationship (self,pkey):

        for i in range(len(self._relationshipset)):
        	for key, value in self._relationshipset[i][0].items():
        		if pkey == value:
        			del self._relationshipset[i]
        			return

        raise Exception ('The relationship with that primary key does not exist')


book = Entity({ "title": "A Distant Mirror",
                          "numberPages": 677,
                          "year": 1972,
                          "isbn": "0345349571" }, ["isbn"])
author = Entity({"firstName": "Neil",
                           "lastName": "Gaiman",
                           "birthYear": 1960 }, ["lastName"])
role = {"book": "Books", "author": "Persons"}
x = RelationshipSet(role, ["date"])
x.create_relationship({"book":{"isbn": "03453"}, "author": {"lastName": "Tuchman"}}, {"date": "911"})
print(x.relationship_keys())
x.create_relationship({"book":{"isbn": "76431"}, "author": {"lastName": "Gaiman"}}, {"date": "112"})
# print(x._relationshipset)
print(x.relationship_keys())
# print(x.read_relationship({"isbn": "03453"}))
x.delete_relationship({"isbn": "03453"})
print(x.relationship_keys())



class Relationship (object):

    def __init__ (self,role_keys,attributes):

        self._role_keys = role_keys
        self._attributes = attributes

    def __str__ (self):

        rkey = lambda r : [ "{}={}".format(name,val) for (name,val) in self._role_keys[r].items() ]
        entities = " ".join([ "[{}]".format("|".join(rkey(r))) for r in self._role_keys ])
        attrs = [ "{}={}".format(name,val) for (name,val) in self._attributes.items() ]
        return "<{} {}>".format(entities,"|".join(attrs))

    def attribute (self,name):
        
        return self._attributes.get(name)

    def role_key (self,role):

        return self._role_keys.get(role)
    
    def primary_key (self):

        return self._role_keys
    


def sample_entities_model ():

    collection = ERModel()

    collection.create_entity_set("Books", ["title", "numberPages", "year", "isbn"], ["isbn"])

    books = collection.read_entity_set("Books")

    books.create_entity({ "title": "A Distant Mirror",
                          "numberPages": 677,
                          "year": 1972,
                          "isbn": "0345349571" })
    
    books.create_entity({ "isbn": "034538623X",
                          "title": "The Guns of August",
                          "year": 1962,
                          "numberPages": 511 })
    
    books.create_entity({ "isbn": "0393356182",
                          "title": "Norse Mythology",
                          "year": 2017,
                          "numberPages": 299 })
     
    books.create_entity({ "isbn": "0060558121",
                          "title": "American Gods",
                          "year": 2003,
                          "numberPages": 591 })
    
    books.create_entity({ "isbn": "0062255655",
                          "title": "The Ocean at the End of the Lane",
                          "year": 2013,
                          "numberPages": 181 })

    books.create_entity({ "isbn": "0060853980",
                          "title": "Good Omens",
                          "year": 1990,
                          "numberPages": 432 })
    
    
    books.create_entity({ "isbn": "0307274939",
                          "title": "The American Civil War",
                          "year": 2009,
                          "numberPages": 396 })

    books.create_entity({ "isbn": "0712666451",
                          "title": "The First World War",
                          "year": 1999,
                          "numberPages": 500})
    
    books.create_entity({ "isbn": "0679768173",
                          "title": "The Kidnapping of Edgardo Mortara",
                          "year": 1997,
                          "numberPages": 350 })
    
    books.create_entity({ "isbn": "0375724886",
                          "title": "The Fortress of Solitude",
                          "year": 2003,
                          "numberPages": 509 })
    
    books.create_entity({ "isbn": "0571205992",
                          "title": "The Wall of the Sky, The Wall of the Eye",
                          "year": 1996,
                          "numberPages": 232 })

    books.create_entity({ "isbn": "1101972120",
                          "title": "Stories of Your Life and Others",
                          "year": 2002,
                          "numberPages": 281 })
    
    books.create_entity({ "isbn": "0812980660",
                          "title": "The War That Ended Peace",
                          "year": 2014,
                          "numberPages": 739 })

    books.create_entity({ "isbn": "0387977102",
                          "title": "Sheaves in Geometry and Logic",
                          "year": 1994,
                          "numberPages": 630})

    books.create_entity({ "isbn": "0387984032",
                          "title": "Categories for the Working Mathematician",
                          "year": 1978,
                          "numberPages": 317})

    books.create_entity({ "isbn": "0060175400",
                          "title": "The Poisonwood Bible",
                          "year": 1998,
                          "numberPages": 560})
    
    
    collection.create_entity_set("Persons", ["firstName", "lastName", "birthYear"], ["lastName"])

    persons = collection.read_entity_set("Persons")

    persons.create_entity({"firstName": "Barbara",
                           "lastName": "Tuchman",
                           "birthYear": 1912 })

    persons.create_entity({"firstName": "Neil",
                           "lastName": "Gaiman",
                           "birthYear": 1960 })

    persons.create_entity({"firstName": "Terry",
                           "lastName": "Pratchett",
                           "birthYear": 1948})

    persons.create_entity({"firstName": "John",
                           "lastName": "Keegan",
                           "birthYear": 1934})

    persons.create_entity({"firstName": "Jonathan",
                           "lastName": "Lethem",
                           "birthYear": 1964})

    persons.create_entity({"firstName": "Margaret",
                           "lastName": "MacMillan",
                           "birthYear": 1943})

    persons.create_entity({"firstName": "David",
                           "lastName": "Kertzer",
                           "birthYear": 1948})

    persons.create_entity({"firstName": "Ted",
                           "lastName": "Chiang",
                           "birthYear": 1967})

    persons.create_entity({"firstName": "Saunders",
                           "lastName": "Mac Lane",
                           "birthYear": 1909})

    persons.create_entity({"firstName": "Ieke",
                           "lastName": "Moerdijk",
                           "birthYear": 1958})

    persons.create_entity({"firstName": "Barbara",
                           "lastName": "Kingsolver",
                           "birthYear": 1955})

    collection.create_relationship_set("AuthoredBy", { "book": "Books",
                                                       "author": "Persons" })
    
    return collection


def sample_relationships_model ():

    collection = sample_entities_model()

    authored = collection.read_relationship_set("AuthoredBy")

    authored.create_relationship({ "book": { "isbn": "0345349571"},
                                   "author": { "lastName": "Tuchman" } })
    
    authored.create_relationship({ "book": { "isbn": "034538623X"},
                                   "author": { "lastName": "Tuchman" } })

    authored.create_relationship({ "book": { "isbn": "0393356182" },
                                   "author": { "lastName": "Gaiman" } })
    
    authored.create_relationship({ "book": { "isbn": "0060558121" },
                                   "author": { "lastName": "Gaiman" } })
    
    authored.create_relationship({ "book": { "isbn": "0062255655" },
                                   "author": { "lastName": "Gaiman" } })

    authored.create_relationship({ "book": { "isbn": "0060853980" },
                                   "author": { "lastName": "Gaiman" } })

    authored.create_relationship({ "book": { "isbn": "0060853980" },
                                   "author": { "lastName": "Pratchett" } })
    
    authored.create_relationship({ "book": { "isbn": "0307274939" },
                                   "author": { "lastName": "Keegan" } })
    
    authored.create_relationship({ "book": { "isbn": "0712666451" },
                                   "author": { "lastName": "Keegan" } })
    
    authored.create_relationship({ "book": { "isbn": "1101972120" },
                                   "author": { "lastName": "Chiang" } })
    
    authored.create_relationship({ "book": { "isbn": "0679768173" },
                                   "author": { "lastName": "Kertzer" } })
    
    authored.create_relationship({ "book": { "isbn": "0812980660" },
                                   "author": { "lastName": "MacMillan" } })
    
    authored.create_relationship({ "book": { "isbn": "0571205992" },
                                   "author": { "lastName": "Lethem" } })
    
    authored.create_relationship({ "book": { "isbn": "0375724886" },
                                   "author": { "lastName": "Lethem" } })
    
    authored.create_relationship({ "book": { "isbn": "0387977102" },
                                   "author": { "lastName": "Mac Lane" } })

    authored.create_relationship({ "book": { "isbn": "0387977102" },
                                   "author": { "lastName": "Moerdijk" } })

    authored.create_relationship({ "book": { "isbn": "0387984032" },
                                   "author": { "lastName": "Mac Lane" } })

    authored.create_relationship({ "book": { "isbn": "0060175400" },
                                   "author": { "lastName": "Kingsolver"} })
    
    return collection


# can't have a call to ._entityset, must replace to get read_entity_set
# APIs erroring and need further testing
# allowed to create sample_entities_model within the last three APIs

def show_title_books_more_500_pages ():
      books = sample_entities_model()
      for book in books.read_entity_set("Books")._entityset:
          if book.attribute("numberPages")>500:
            print(book.attribute("title"))


def show_title_books_by_barbara ():
    relations = sample_relationships_model()
    books = sample_entities_model()
    temp = []
    for relation in relations.read_relationship_set("AuthoredBy"):
    	if relation.get("author").get("lastName") == "Tuchman":
    		temp.append(relation.get("author").get("isbn"))

    for book in books.read_entity_set("Books")._entityset:
    	if book.attribute("isbn") in temp:
    		print(book.attribute("title"))


def show_name_authors_more_one_book ():
	relations = sample_relationships_model()
	books = sample_entities_model()
	temp = []
	authors = []
	for relation in relations.read_relationship_set("AuthoredBy"):
		if relation.get("author").get("lastName") in temp:
			authors.append(relation.get("author").get("isbn"))
		else:
			temp.append(relation.get("author").get("lastName"))

	for book in books.read_entity_set("Books")._entityset:
		if book.attribute("isbn") in authors:
			print(book.attribute("title"))

                
def show_title_books_more_one_author ():
	relations = sample_relationships_model()
	books = sample_entities_model()
	temp = []
	books = []
	for relation in relations.read_relationship_set("AuthoredBy"):
		if relation.get("author").get("isbn") in temp:
			authors.append(relation.get("author").get("isbn"))
		else:
			temp.append(relation.get("author").get("isbn"))

	for book in books.read_entity_set("Books")._entityset:
		if book.attribute("isbn") in authors:
			print(book.attribute("title"))

     
# show_title_books_more_500_pages ()
#show_title_books_by_barbara ()

def tests (): 
    
    print("----------------------------------------")
    show_title_books_more_500_pages()
    
    print("----------------------------------------")
    show_title_books_by_barbara()
    
    print("----------------------------------------")
    show_name_authors_more_one_book()
    
    print("----------------------------------------")
    show_title_books_more_one_author()

# c = sample_entities_model()

# for pk in c.read_entity_set("Persons").entity_keys():
#   print(c.read_entity_set("Persons").read_entity(pk))
