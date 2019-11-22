# processes medline journal information in an article

'''
As the medline journal is like, in structure, pubmed_article, we follow the
same approach, and, after we populate the medline journal row, we return the
id for storage in the pubmed_article table
'''

from common.db import fetch_or_add,build_then_insert

from processors.xml_util import text_processor,tagged_text_processor,redirect
from processors.xml_util import redirector

def medical_journal_info_processor(cursor,elt,vals):
   rd = redirector(cursor,elt,vals)
   med0 = { }
   med1 = rd(med0,'NlmUniqueID','nlm_unique_id')
   if med1:
      vals = due_process(cursor,elt,vals,med1,rd)
   return vals

def due_process(cursor,elt,vals,med1,rd):
   mji_id = None
   stmt='SELECT id FROM medline_journal_info_lk WHERE nlm_unique_id=%s'
   cursor.execute(stmt,(med1['nlm_unique_id'],))
   if cursor.rowcount > 0:
      mji_id = cursor.fetchone()[0]
   else:
      med2 = redirect(cursor,elt,med1,'Country',country_processor)
      med3 = rd(med2,'ISSNLinking','issn_linking')
      mji_id = build_then_insert(cursor,'medline_journal_info_lk',med3)
   vals['medline_journal_info_id'] = mji_id
   return vals

def country_processor(cursor,elt,vals):
   cntr = elt.text
   cntr_id = fetch_or_add(cursor,'country_lk','country',cntr)
   vals['country_id'] = cntr_id
   return vals
