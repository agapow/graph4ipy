"""
Reading and writing JGF format graphs.
"""

### IMPORTS

import json


### CONSTANTS & DEFINES

### CODE ###

class JgfReader (object):
   # XXX: maybe look at a custom decoder/loader?

   def parse (self, str_or_file):
      # NOTE: try to decode multiple objects: MultiGraph, SingleGraph or Graph
      # XXX: do we need specialised decoders for each?

      if hasattr (str_or_file, 'read'):
         buf = str_or_file.read()
      else:
         buf = str_or_file
      json_obj = json.loads (buf)

      # what am I looking at?
      assert type (json_obj) == dict, \
         "expected top level JSON object to be a dict, actually a '%s'" % type (json_obj)
      json_keys = json_obj.keys()
      if 'graphs' in json_keys:
         return self.parse_multigraph (json_obj)
      if 'graphs' in json_keys:
         return self.parse_multigraph (json_obj)
      if 'graphs' in json_keys:
         return self.parse_multigraph (json_obj)

   def parse_multigraph (self, json_obj):
      graphs = [self.parse_graph (g) for g in json_obj['graphs']]
      return MultiGraph (
         graphs=graphs,
         mgraph_type=json_obj.get ('type', None),
         label==json_obj.get ('label', None),
         **json_obj.get ('metadata', {})
      )

   def parse_singlegraph (self, json_obj):
      graph = [self.parse_graph (g) for g in json_obj['graph']]
      return MultiGraph (
         graph=graph,
         graph_type=json_obj.get ('type', None),
         label==json_obj.get ('label', None),
         **json_obj.get ('metadata', {})
      )

   def parse_graph (self, json_obj):
      pass
