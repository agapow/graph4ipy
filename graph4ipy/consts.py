"""
Module-file constants.
"""

### IMPORTS

import os

# XXX: or should we not allow this?
__all__ = (
   'MODULE_PATH',
   'ASSETS_PATH',
)

### CONSTANTS & DEFINES

MODULE_PATH = os.path.normpath (os.path.dirname (__file__))
ASSETS_PATH = os.path.join (MODULE_PATH, 'assets')


### CODE ###

### END ###
