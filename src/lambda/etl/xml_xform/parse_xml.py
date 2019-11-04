import xml.etree.ElementTree as ET

def parse_row(row_id, row_xml):
   print('parsing xml for row',row_id)
   skml = ET.fromstring(row_xml)

   # do some other stuff or nah?
   return skml
