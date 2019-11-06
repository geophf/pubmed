# stores the XML which we parsed

from common.db import fetch_or_add

def store_row(cursor,row_id,skml,yn_lk):
   fns = load_processors(cursor)
   vals = { }
   print('Storing XML for row',row_id)
   dispatcher(cursor,'MedlineCitation',fns,skml,vals)
   dispatcher(cursor,'PubmedData',fns,skml,vals)
   print('My data model')
   for (k,v) in vals.items():
      print("\t",k,':',v)

def dispatcher(cursor,name,fns,skml,vals):
   print('scanning',name)
   for elt in skml.findall(name):
      for e1 in elt:
         tg = e1.tag
         f = fns.get(tg)
         if f:
            print('for',tg,'I get',f)
            vals = globals()[f['processor']](cursor,e1,vals)
         else:
            print('I have no dispatch for',tg)
   return vals

def load_processors(cursor):
   fn_map = { }
   stmt='SELECT xml_element,processor,"table","column" FROM xml_element_map'
   cursor.execute(stmt)
   for row in cursor.fetchall():
      dic = { }
      dic['processor'] = row[1]
      dic['table'] = row[2]
      dic['column'] = row[3]
      fn_map[row[0]] = dic
   return fn_map

def pub_status_processor(cursor,elt,vals):
   stat = elt.text
   pub_id = fetch_or_add(cursor,'publication_status_lk','status',stat)
   return kv('publication_status_ind',vals,pub_id)

def pmid_processor(cursor,elt,vals):
   return text_processor(elt,'pmid',vals)

def text_processor(elt,col,vals):
   return kv(col,vals,elt.text)

def kv(col,vals,val):
   vals[col] = val
   return vals

def simple_inserter(cursor,table,column,val):
   stmt='INSERT INTO ' + table + ' (' + column + ') VALUES (%s) RETURNING id'
   cursor.execute(stmt,(val,))
   return cursor.fetchone()[0]
