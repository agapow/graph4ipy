"""
Working with cytoscape.js data.
"""

# TODO: load from Python
# TODO: load from JSON

### IMPORTS

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import object

from . import jsonutils

__all__ = (
   'CytoJson',
)


### CONSTANT & DEFINES

# all other keys are pushed into 'data'
NONDATA_KEYS = (
   'position'
   'group',
   'removed',
   'selected',
   'selectable',
   'locked',
   'grabbed',
   'grabbable',
   'classes',
)


### CODE ###

class CytoJson (object):
   def __init__ (self, container):
      # XXX: how to stop container line from being escaped?
      self._json = {
         'container': container,
         'layout': {},
         'style': [],
         'elements': [],
      }
      # just to keep track of what ids have been used
      self._node_ids = []
      self._edge_ids = []

   def add_layout (self, key, val):
      # TODO: assert key is string and val is str or number?
      self._json['layout']['key'] = val

   def add_style (self, selector, style_dict):
      # TODO: assert selector is string and styles is dict?
      self._json['style'].append ({
         'selector': selector,
         'style': style_dict,
      })

   def add_element (self, elem_id=None, elem_type=None, classes=None, **kwargs):
      # NOTE: validation for ids etc. only takes place in specialised fxns,
      # This fxn only checks for duplicate ids
      # NOTE: although id, type & classes are not required, we list them here
      # to encourage them

      ## Preconditions:
      assert (elem_type is None) or (elem_type in ('nodes', 'edges'))

      ## Main:
      new_elem = {}

      # positional args
      if elem_id is not None: new_elem['id'] = elem_id
      if elem_type is not None: new_elem['groups'] = elem_type
      if classes is not None:
         if type (classes) in (list, tuple):
            classes = ' '.join (classes)
         new_elem['classes'] = classes

      # sort all others into data / non-data
      new_elem['data'] = {}
      for k, v in list (kwargs.items()):
         if k in NONDATA_KEYS:
            assert k not in new_elem, \
               "writing value to element key '%s' twice" % k
            new_elem[k] = v
         else:
            new_elem['data'][k] = v

      # add to existing
      self._json.append (new_elem)

      ## Postconditions & return:
      return new_elem

   def add_node (self, node_id=None, classes=None, **kwargs):
      # NOTE: although id and classes are not required, we list them here
      # to encourage them
      ## Main:
      new_node = self.new_elem (elem_id=node_id, elem_type='nodes',
         classes=classes, **kwargs)

      ## Postconditions & return:
      new_id = new_node['data'].get ('id')
      if new_id is not None:
         assert new_id not in self._node_ids, \
            "duplicate node id '%s'" % new_id
         self._node_ids.append (new_id)

      return new_node


   def add_edge (self, from_node, to_node, edge_id=None, classes=None, **kwargs):
      # NOTE: although id and classes are not required, we list them here
      # to encourage them
      ## Main:
      new_edge = self.new_elem (elem_id=edge_id, elem_type='edges',
         classes=classes, source=from_node, target=to_node, **kwargs)
      ## Postconditions & return:
      new_id = new_edge['data'].get ('id')
      if new_id is not None:
         assert new_id not in self._edge_ids, \
            "duplicate node id '%s'" % new_id
         self._edge_ids.append (new_id)
      src_id = new_edge['data']['source']
      assert src_id in self._node_ids, \
         "edge from unknown node '%s'" % src_id
      assert target_id in self._node_ids, \
         "edge to unknown node '%s'" % target_id

      return new_node

   def to_json (self):
      # TODO: pretty print options?
      return jsonutils.ExtEncoder (self._json)


### END ###
