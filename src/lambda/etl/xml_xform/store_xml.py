import datetime

from processors.util import text_processor, redirect, kv
from processors.db_util import fetch_xml_dict,lookup_xml_id,load_processors

# stores the XML which we parsed

from common.db import fetch_or_add

'''
A 'row' is a rather complicated affair because the XML hierarchical model does
not match the relational model in the database, so, to store a row, we first
have to populate the pubmed_article table, get the id from that row, that use
that key to index off the join and auxiliary tables associated with that 
abstract.

This, then, ends up as a two-pass system ('compiler,' if you will): one pass
through the XML to get the first-tier pubmed_article data, then the second
pass through the same XML, but this time with the pubmed_article row id, to
get the associated/auxiliary data.
'''

def store_row(cursor,row_id,skml,yn_lk):
   fns = load_processors(cursor)
   vals = { 'abstract_stg_id' : row_id }
   path = '/PubmedArticle/'
   print('Storing XML for row',row_id)
   xdict = fetch_xml_dict(cursor)
   (vals1,xd1) = dispatcher(cursor,'MedlineCitation',fns,skml,vals,path,row_id,xdict)
   (vals2,xd2) = dispatcher(cursor,'PubmedData',fns,skml,vals1,path,row_id,xd1)
   print('My data model')
   for (k,v) in vals2.items():
      print("\t",k,':',v)

# dispatches to XML element processors for the children of this element

def dispatcher(cursor,name,fns,skml,vals,path,art_id,xdict):
   print('scanning',name)
   path1 = path + name + '/'
   xd1 = xdict
   for elt in skml.findall(name):
      for e1 in elt:
         tg = e1.tag
         path2 = path1 + tg + '/'
         f = fns.get(tg)
         if f:
            print('for',tg,'I get',f)
            vals = globals()[f['processor']](cursor,e1,vals)
         else:
            xd1 = log_no_processor(cursor,path1,tg,art_id,xd1)
   return (vals,xd1)

# if we don't have a processor for this element, log this in the database

def log_no_processor(cursor,path1,tg,art_id,xdict):
   print('Logging I have no dispatch for',tg)
   (key,xd1) = lookup_xml_id(cursor,path1,tg,xdict)
   stmt='''
INSERT INTO not_mapped (article_stg_id,xml_element_id) VALUES (%s,%s)
'''
   cursor.execute(stmt,(art_id,key))
   return xd1

# ----- PROCESSORS ------------------------------------------------------------

def pub_status_processor(cursor,elt,vals):
   stat = elt.text
   pub_id = fetch_or_add(cursor,'publication_status_lk','status',stat)
   return kv('publication_status_ind',vals,pub_id)

def pmid_processor(cursor,elt,vals):
   return text_processor(elt,'pmid',vals)

def nlm_id_processor(cursor,elt,vals):
   return text_processor(elt,'nlm_unique_id',vals)

def article_processor(cursor,elt,vals):
   return redirect(cursor,elt,vals,'ELocationID',e_location_processor)

def medical_journal_info_processor(cursor,elt,vals):
   return redirect(cursor,elt,vals,'NlmUniqueID',nlm_id_processor)

# whew! Lookup-table value (with possible insert) then keyed return!

def e_location_processor(cursor,eloc,vals):
   typ = eloc.attrib['EIdType']
   e_id_type = fetch_or_add(cursor,'article_id_lk','id_kind',typ)
   val = eloc.text
   stmt='''
INSERT INTO article_id (id_type,id_value)
VALUES (%s,%s)
RETURNING id
'''
   cursor.execute(stmt,(e_id_type,val))
   res = cursor.fetchone()[0]
   vals['e_location_id'] = res
   return vals
