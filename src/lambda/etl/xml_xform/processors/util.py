# a set of utilities for parsing and storing the XML for a pubmed abstract

# this function says: 'For this child element, use this processor.' A redirect

def redirect(cursor,elt,vals,child,processor):
   found = False
   for ad in elt.findall(child):
      vals = processor(cursor,ad,vals)
      found = True
   if not found:
      print('No child element',child,'found for',elt.tag)
   return vals

# grabs and stores the content of an element

def text_processor(elt,col,vals):
   return kv(col,vals,elt.text)

'''
dates in pubmed abstracts are in this format:

<DateRevised>
<Year>2018</Year>
<Month>12</Month>
<Day>12</Day>
</DateRevised>

We parse the date and return a date value with this call:

   vals = date_processor(elt,'publish_dt',vals)
'''

def date_processor(elt,col,vals):
   datemap = xlate_kids(elt)

   def d(field):
      return int(datemap[field])

   dt = datetime.datetime(d('Year'),d('Month'),d('Day')).date()

   # Ya see how I did that? FUNCTIONALS, BAYBEE! FUNCTIONALS!

   return kv(col,vals,dt)

# a simple dictionary assignment functional

def kv(col,vals,val):
   vals[col] = val
   return vals

# An XML-to-dict translation

def xlate_kids(elt):
   ans = { }
   for kid in elt:
      ans[kid.tag] = kid.text
   return ans
