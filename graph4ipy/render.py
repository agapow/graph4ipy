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
from os import path
import uuid
import webbrowser
# exposed by future
from urllib.parse import urljoin
from urllib.request import pathname2url

import IPython
from IPython.display import HTML, display

from . import utils
from . import jsonutils

__all__ = (
   'draw',
   'draw_in_browser',
)


### CONSTANT & DEFINES

IPYTHON_VERSION = IPython.release.version


### CODE ###

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

         html_filename = path.join (tempdir, 'index.html')
         with open(html_filename, 'wb') as f:
            f.write(html)

         libs = (('server', 'css', 'chosen.css'),
               ('server', 'css', 'server.css'),
               ('js', 'jquery-1.11.1.min.js'),
               ('server', 'js', 'chosen.jquery.min.js'),
               ('js', 'build', 'imolecule.min.js'))
         for lib in libs:
            shutil.copy (path.join(file_path, *lib), tempdir)

         html_file_url = urljoin('file:', pathname2url(html_filename))

         print('Opening html file: {}'.format(html_file_url))
         webbrowser.open(html_file_url)
      else:
         # We're running in ipython: display widget
         display(HTML(html))
   else:
      return html

def draw_in_browser (data, styles=None, title='graph4ipy', work_dir=None, tmp_dir=False,
      file_name='graph.html'):
   """
   Generate a webpage containing the graph.

   Args:
      data: object or data to be displayed in graph
      styles: Python (not JSON) list of style dictionaries
      title: title of webpage
      work_dir: directory for webpage to be created in
      temp_dir: create webpage in temporary directory
      file_name: name of generated webpage

   """
   ## Preconditions & preparation:
   assert not (work_dir) and not (tmp_dir), \
      "can supply at most one of work_dir and tmp_dir"
   if tmp_dir:
      work_dir = tempfile.mkdtemp ('graph4ipy')
   else:
      if work_dir is None:
         work_dir = '.'

   ## Main:
   # TODO: allow creation in temp dir
   # TODO: allow self_contained (included files)
   # TODO: copy assets files
   # TODO: allow naming of target file

   # obtain styles
   cyto_style_str = utils.load_asset ('default.cyto-style.json')
   cyto_style_json = utils.load_json ('default.cyto-style.json')
   cyto_style_str = jsonutils.py_to_json (cyto_style_json)

   # parse data
   with open ('tests/data/genemania.json', 'r') as in_hndl:
      elements_str = in_hndl.read()

   # load & render page template
   page_tmpl = utils.load_template ('webpage.template.html')
   rendered_page = page_tmpl.substitute ({
      'title': title,
      'cyto_style': cyto_style_str,
      'element_data': elements_str,
      'jquery_tag': consts.JQUERY_TAG,
      'cyto_tag': consts.CYTO_TAG
   })

   # write out resultant page
   target_page = path.abspath (path.join (work_dir, file_name))
   with open (target_page, 'w') as out_hndl:
      out_hndl.write (rendered_page)

   # open in browser
   page_url = urljoin ('file:', pathname2url (target_page))
   webbrowser.open (page_url)





### END ###
