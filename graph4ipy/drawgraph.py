"""
Draw a graph or graph-like object in an iPython notebook or browser.
"""

### IMPORTS

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()

import os
import uuid
# exposed by future
from urllib.parse import urljoin
from urllib.request import pathname2url

import IPython
from IPython.display import HTML, display

__all__ = (
   'draw',
   'draw_in_browser',
)


### CONSTANT & DEFINES

IPYTHON_VERSION = IPython.release.version



file_path = os.path.normpath (os.path.dirname (__file__))
local_path = 'nbextensions/imolecule.min.js'
remote_path = ('https://rawgit.com/patrickfuller/imolecule/master/'
            'imolecule/js/build/imolecule.min.js')

### CODE ###

# always executed
# code flinched from imolecule
if IPYTHON_VERSION < '2.0':
   raise ImportError ("Old version of IPython detected. Please update.")
else:
   try:
      if IPYTHON_VERSION < '4.0':
         from IPython.html.nbextensions import install_nbextension
      else:
         from notebook.nbextensions import install_nbextension
         # TODO: look this up
      p = os.path.join (file_path, 'assets', PATH_TO_JS_AND_CSS)
      install_nbextension ([p] if IPYTHON_VERSION < '3.0' else p, verbose=0)
   except:
      pass


def draw (data):
   """
   Draws graph or graph-like object.

   """
   # convert or wrangle data

   # generate unique id for div
   div_id = uuid.uuid4()

   # fill in
   html = """<div id="molecule_%s"></div>
         <script type="text/javascript">
         require.config({baseUrl: '/',
                     paths: {imolecule: ['%s', '%s']}});
         require(['imolecule'], function () {
            var $d = $('#molecule_%s');
            $d.width(%d); $d.height(%d);
            $d.imolecule = jQuery.extend({}, imolecule);
            $d.imolecule.create($d, {drawingType: '%s',
                              cameraType: '%s',
                              shader: '%s',
                              showSave: %s});
            $d.imolecule.addElements(%s);
            $d.imolecule.draw(%s);

            $d.resizable({
               aspectRatio: %d / %d,
               resize: function (evt, ui) {
                  $d.imolecule.renderer.setSize(ui.size.width,
                                        ui.size.height);
               }
            });
         });
         </script>""" % (div_id, local_path[:-3], remote_path[:-3],
                     div_id, size[0], size[1], drawing_type,
                     camera_type, shader,
                     'true' if show_save else 'false',
                     json_element_properties,
                     json_mol, size[0], size[1])

   # Execute js and display the results in a div (see script for more)
   if display_html:
      try:
         __IPYTHON__
      except NameError:
         # We're running outside ipython, let's generate a static HTML and
         # show it in the browser
         import shutil
         import webbrowser
         from tempfile import mkdtemp
         from time import time

         from tornado import template

         # better template handling
         t = template.Loader(file_path).load('viewer.template')
         html = t.generate(title="imolecule", json_mol=json_mol,
                       drawing_type=drawing_type, shader=shader,
                       camera_type=camera_type,
                       json_element_properties=json_element_properties)

         tempdir = mkdtemp(prefix='imolecule_{:.0f}_'.format(time()))

         html_filename = os.path.join(tempdir, 'index.html')
         with open(html_filename, 'wb') as f:
            f.write(html)

         libs = (('server', 'css', 'chosen.css'),
               ('server', 'css', 'server.css'),
               ('js', 'jquery-1.11.1.min.js'),
               ('server', 'js', 'chosen.jquery.min.js'),
               ('js', 'build', 'imolecule.min.js'))
         for lib in libs:
            shutil.copy(os.path.join(file_path, *lib), tempdir)

         html_file_url = urljoin('file:', pathname2url(html_filename))

         print('Opening html file: {}'.format(html_file_url))
         webbrowser.open(html_file_url)
      else:
         # We're running in ipython: display widget
         display(HTML(html))
   else:
      return html

def draw_in_browser (data):
   pass


### END ###
