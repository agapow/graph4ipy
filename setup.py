from setuptools import setup
from graph4ipy import __version__

setup(
   name="graph4ipy",
   version=__version__,
   description="Display graphs from the IPython notebook.",
   url="http://www.agapow.net/software/graph4py",
   license="MIT",
   author="Paul Agapow",
   author_email="paul@agapow.net",
   # package_dir={
   #    "imolecule": "imolecule",
   #    "imolecule.server": "imolecule/server",
   #    "imolecule.js": "imolecule/js"
   # },
   # package_data={
   #    "imolecule.js": ["imolecule/js/build/imolecule.min.js"],
   #    "imolecule.server": [
   #       "imolecule/server/data/*.json",
   #       "imolecule/server/js/*.js",
   #       "imolecule/server/css/*.css",
   #       "imolecule/server/*.template",
   #       "imolecule/*.template"
   #    ]
   # },
   include_package_data=True,
   packages=["graph4py"],
   install_requires=[
      "ipython",
      #"tornado",
   ],
   entry_points={
   },
   classifiers=[
      "Natural Language :: English",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Framework :: IPython",
      "Topic :: Scientific/Engineering :: Visualization"
   ]
)
