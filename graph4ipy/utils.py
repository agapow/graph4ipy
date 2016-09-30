"""
Various module-wide utilities.
"""

### IMPORTS

from os import path
from string import Template
import json

from . import consts

__all__ = (
   'load_asset',
   'load_template',
)


### CONSTANTS & DEFINES

### CODE ###

def load_asset (pth):
   """
   Read in file in the assets directory.
   """
   asset_path = path.join (consts.ASSETS_PATH, pth)
   assert path.isfile (asset_path), \
      "file '%s' does not exist or is not a file" % asset_path
   with open (asset_path, 'rU') as in_hndl:
      return in_hndl.read()


def load_template (pth):
   """
   Read in a template defined in a file in the assets directory.
   """
   tmpl_str = load_asset (pth)
   return Template (tmpl_str)


def load_json (pth):
   """
   Read in a JSON file and convert to Python equivalents.
   """
   json_str = load_asset (pth)
   return json.loads (json_str)


### END ###
