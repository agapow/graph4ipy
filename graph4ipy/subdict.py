

## Utils
# Some functions to allow more terse definition of properties

def _d_get (k): return lambda s: dict.get (s, k, None)
def _d_get_def (k,d): return lambda s: dict.get (s, k, d)
def _d_getitem (k): return lambda s: dict.__getitem__ (s, k)
def _d_setitem (k): return lambda s,v: dict.__setitem__ (s, k, v)


class Subdict (dict):
   """
   A dictionary that stores some fields at top level, some in a sub-dictionary.

   Some of the graph formats features data that is a map, but with only a
   certain set, fixed set of fields at the toplevel. Other fields are banished
   to a contained dictionary with a fixed name. With
   """
   subkey = 'metadata'
   topfields = ['foo', 'bar']

   def __init__ (self, *args, **kwargs):
      super (Subdict, self).__init__()
      self._subdict = None
      self._init_subdict()
      print (self)

   def _init_subdict (self):
      self._subdict = {}
      super (Subdict, self).__setitem__(self.__class__.subkey,
         self._subdict)

   def __getitem__ (self, k):
      if k in self.__class__.topfields:
         return super (Subdict, self).__getitem__(k)
      else:
         return self._subdict[k]
      print (self)

   def __setitem__ (self, k, v):
      if k in self.__class__.topfields:
         super (Subdict, self).__setitem__(k, v)
      else:
         self._subdict[k] = v
      print (self)



class MultiGraph (dict):
   # NOTE: JGF refers to this as "graphs" but we need more clarity
   subkey = 'metadata'
   topfields = ['type', 'label', 'graphs']

   metadata = property (_d_get('metadata'), _d_setitem ('metadata'))
   type = property (_d_get('type'), _d_setitem ('type'))
   label = property (_d_get('labels'), _d_setitem ('labels'))
   graphs = property (_d_get('graphs'), _d_setitem ('graphs'))

   def __init__ (self, graphs=None):
      self.graphs = graphs or []


class SingleGraph (dict):
   """
   Data (and JSON) for a single graph in JGF format.
   """

   graph = property (
      lambda s,k: dict.get (s, k, None),
      lambda s,k,v: dict.__setitem__ (s, k, v),
   )

   def __init__ (self, graph=None):
      if graph:
         self.graph = graph

   def __setitem__ (self, k, v):
      assert k == 'graph', \
         "graph json only accepts 'graph' key not '%s'" % k



class Graph (Subdict):
   # XXX: there a bit of weirdness here in that a graph can be the naked
   # dict, where it's an item in the MultiGraph list or appear as a single
   # graph in which case it's a dict with a single key 'graph'. Thus, this
   # is really a GraphData class and we need a SingleGraph class as above.

   subkey = 'metadata'
   topfields = ['type', 'label', 'directed', 'nodes', 'edges']

   metadata = property (_d_get('metadata'), _d_setitem ('metadata'))
   type = property (_d_get('type'), _d_setitem ('type'))
   label = property (_d_get('labels'), _d_setitem ('labels'))
   directed = property (_d_get('directed'), _d_setitem ('directed'))
   nodes = property (_d_get('nodes'), _d_setitem ('nodes'))
   edges = property (_d_get('edges'), _d_setitem ('edges'))

   def __init__ (self, label=None, graph_type=None, directed=None,
         nodes=None, edges=None, **kwargs):
      self.label = label
      self.type = graph_type
      self.directed = directed
      self.nodes = nodes or []
      self.edges = edges or []
      self.metadata = kwargs

   def add_node (self, node_id, label=None, node_type=None, **kwargs):
      ## Main:
      new_node = Node (node_id=node_id, label=label, node_type=node_type,
         **kwargs)
      self.nodes.append (new_node)

      ## Postconditions & return:
      return new_node

   def add_edge (self, source, target, edge_id=None, directed=None,
         relation=None, **kwargs):

      ## Main:
      new_edge = Edge (source=source, target=target, edge_id=edge_id,
         directed=directed, relation=relation, **kwargs)

      ## Postconditions & return:
      return new_edge


class Node (Subdict):
   subkey = 'metadata'
   topfields = ['id', 'label', 'type']

   metadata = property (_d_get('metadata'), _d_setitem ('metadata'))
   type = property (_d_get('type'), _d_setitem ('type'))
   id = property (_d_get('id'), _d_setitem ('id'))
   label = property (_d_get('label'), _d_setitem ('label'))

   def __init__ (self, node_id, label=None, node_type=None, **kwargs):
      self.label = label
      self.type = graph_type
      self.id = id
      self.metadata = kwargs


class Edge (Subdict):
   subkey = 'metadata'
   topfields = ['id', 'source', 'target', 'directed', 'relation']

   metadata = property (_d_get('metadata'), _d_setitem ('metadata'))
   type = property (_d_get('type'), _d_setitem ('type'))
   id = property (_d_get('id'), _d_setitem ('id'))
   label = property (_d_get('label'), _d_setitem ('label'))

   def __init__ (self, source, target, edge_id=None, directed=None,
         relation=None, **kwargs):
      self.relation = relation
      self.source = source
      self.target = target
      self.directed = directed
      self.id = edge_id
      self.metadata = kwargs
