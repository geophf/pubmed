# processes information in the Article element of the pubmed abstract XML

from common.db import fetch_or_add

from processors.util import text_processor,tagged_text_processor,redirect
from processors.util import redirector

def article_processor(cursor,elt,vals):
   rd = redirector(cursor,elt,vals)
   vals1 = rd(vals,'ArticleTitle','article_title')
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

'''

# language_processor is like the e_location_processor, but simpler, thank
# goodness!

WRONG! There can be multiple languages for an article, so we have to stage2
this

def language_processor(cursor,lang,vals):
   ell = lang.text
   lang_id = fetch_or_add(cursor,'language_lk','language',ell)
   print('Got',lang_id,'for language',ell)
   vals['language_id'] = lang_id
   return vals
'''

# REEEEEE! abstract text is buried two elements deep! REEEE!

def abstract_processor(cursor,elt,vals):
   return redirect(cursor,elt,vals,'AbstractText',abstract_text_processor)

def abstract_text_processor(cursor,elt,vals):
   return text_processor(elt,'abstract_text',vals)
