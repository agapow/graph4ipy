"""
A series of handlers for various converters to the cytoscape.js format.
"""

### IMPORTS

### CONSTANTS & DEFINES

### CODE ###

class GraphJsonToCyto (object):
   def __init__ (self):
      pass

   def convert (self, data):
      """
      Convert GraphJSON to the cytoscape.js format.

      Args:
         data: GraphJSON as Python objects (i.e. not a string)

      Returns:
         a CytoJson object

      """
      new_cyto = CytoJson()
      for n in data['nodes']:
         new_cyto.add_node (node_id)
      for n in data['edges']:
         new_cyto.add_edge (node_id)



### END ###
