# processes information in the Article element of the pubmed abstract XML

from common.db import fetch_or_add

from processors.util import text_processor, redirect

def article_processor(cursor,elt,vals):
   def redirector(v,elt_nm,col_nm):
      return redirect(cursor,elt,v,elt_nm,tagged_text_processor(col_nm))

   vals1 = redirector(vals,'ArticleTitle','article_title')
   vals2 = redirect(cursor,elt,vals1,'Abstract',abstract_processor)
   return redirect(cursor,elt,vals2,'ELocationID',e_location_processor)

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

def tagged_text_processor(col_nm):
   def tagging_fn(cursor,elt,vals):
      return text_processor(elt,col_nm,vals)
   return tagging_fn

# REEEEEE! abstract text is buried two elements deep! REEEE!

def abstract_processor(cursor,elt,vals):
   return redirect(cursor,elt,vals,'AbstractText',abstract_text_processor)

def abstract_text_processor(cursor,elt,vals):
   return text_processor(elt,'abstract_text',vals)
