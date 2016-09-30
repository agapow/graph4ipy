"""
IPython-specific code, in particular loading & unloading.

"""

### IMPORTS

### CONSTANTS & DEFINES

### CODE ###

def load_ipython_extension (ipython):
   global _loaded
   if not _loaded:
      #ip.register_magics(BlockdiagMagics)
      _loaded = True


def unload_ipython_extension (ipython):
   # If you want your extension to be unloadable, put that logic here.
   pass


### END ###
