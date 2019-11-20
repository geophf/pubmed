# a set of database utilities for processing pubmed XML abstracts

'''
creates a custom dictionary of ((xpath,xml-element), id)

... but we also need to add new elements, get the new id, as we go

The key being a cartesian product renders the standard SQL dictionary functions
useless, so I have to write custom storage and retrieval functions here.
'''

def fetch_xml_dict(cursor):
   print('fetching xml_element dictionary')
   stmt='SELECT xpath,xml_element,id FROM xml_element'
   cursor.execute(stmt)
   print('dictionary has',cursor.rowcount,'entries')
   rows = cursor.fetchall()
   ans = { }
   for row in rows:
      ans[(row[0],row[1])] = row[2]
   return ans

def lookup_xml_id(cursor,path,elt,dict):
   key = (path,elt)
   ans = dict.get(key)
   if not ans:
      print('adding',path,elt,'to xml_element dictionary.')
      stmt='''
INSERT INTO xml_element (xpath,xml_element)
VALUES (%s,%s)
RETURNING id
'''

      cursor.execute(stmt,(path,elt))
      ans = cursor.fetchone()[0]
      dict[key] = ans
   return (ans,dict)

# loads the processor functions for each XML element from the database

def load_processors(cursor):
   fn_map = { }
   stmt='''
select a.xml_element,b.processor,b.table_nm,b.column_nm
from xml_element a
join xml_element_map b on b.xml_element_id=a.id
'''

   cursor.execute(stmt)
   for row in cursor.fetchall():
      dic = { }
      dic['processor'] = row[1]
      dic['table'] = row[2]
      dic['column'] = row[3]
      fn_map[row[0]] = dic
   return fn_map
