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

JQUERY_TAG = """<script src="http://code.jquery.com/jquery-3.1.1.min.js"
   integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
   crossorigin="anonymous"></script>"""
CYTO_TAG = """<script src="graph4ipy/assets/cytoscape.js"></script>"""

### CODE ###

### END ###
