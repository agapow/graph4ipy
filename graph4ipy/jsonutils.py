"""
Various utilities for working with JSON.

The main issue that prompted the code here was the need to emit JSON that
included variables and other literal strings. To do this we have to mark
such values and customize the emitter.

"""

### IMPORTS

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object

import json

__all__ = (
    'JsonLiteral',
    'ExtEncoder',
    'py_to_json'

)


### CONSTANT & DEFINES


### CODE ###

class JsonLiteral (object):
   def __init__ (self, data):
      self.data = data


class ExtEncoder (json.JSONEncoder):
   # TODO: custom key sorting?

   def default (self, obj):
      if isinstance (obj, JsonLiteral):
         return obj.data
      else:
         # otherwise baseclass
         return json.JSONEncoder.default (self, obj)


def py_to_json (data, *args, **kwargs):
   return ExtEncoder (*args, **kwargs).encode (data)


### END ###
