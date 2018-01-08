Here lie the source files for the UCD Mechanical Engineering senior capstone
design course that is organized by Jason K. Moore.

Editing On Github
=================

Navigate to the ``.rst`` file you want to change in the ``content`` directory
and press the pencil to edit the file. The formatting should follow the rules
of restructuredText (`example guide
<http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_). Once, done
submit a pull request and wait to see if the page properly builds. If it
builds, then merge the pull request. If it fail, then edit the files in the
pull request to fix the errors and try again.

Local Build Instructions
========================

Install miniconda_, add the Conda Forge channel, and create an environment for
Pelican sites::

   $ conda config --add channels conda-forge
   $ conda create -n pelican python=2 pelican fabric ghp-import
   $ source activate pelican

Clone the plugin repository::

   (pelican)$ mkdir ~/src
   (pelican)$ git clone git@github.com:getpelican/pelican-plugins.git ~/src/pelican-plugins

Rebuild and serve the site locally::

   (pelican)$ fab reserve

.. _miniconda: http://conda.pydata.org/miniconda.html

License
=======

The text, images, contents, and source of the website are released under the
Creative Commons Zero License (public domain) unless otherwise specified.
