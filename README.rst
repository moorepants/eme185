Here lie the source files for the UCD Mechanical Engineering senior capstone
design course that is organized by Jason K. Moore.

Build Instructions
==================

Install miniconda_, add the Conda Forge channel, and create an environment for
Pelican sites::

   $ conda config --add channels conda-forge
   $ conda create -n pelican python=2 pelican fabric ghp-import
   $ source activate pelican

Clone the plugin repository::

   (pelican)$ mkdir ~/src
   (pelican)$ git clone git@github.com:getpelican/pelican-plugins.git ~/src/

Rebuild and serve the site locally::

   (pelican)$ fab reserve

Push the site to Github pages::

   (pelican)$ fab gh_pages

.. _miniconda: http://conda.pydata.org/miniconda.html

License
=======

The text, images, contents, and source of the website are released under the
Creative Commons Zero License (public domain) unless otherwise specified.
