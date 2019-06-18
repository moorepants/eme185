Introduction
============

Here lie the source files for the UCD Mechanical Engineering senior capstone
design course that is organized and taught by Jason K. Moore.

The latest version of the website can be viewed at:

http://moorepants.github.io/eme185/

Versions for prior years are at:

- http://moorepants.github.io/eme185/2019
- http://moorepants.github.io/eme185/2018
- 2017 and 2016 do not yet have archived sites.

License
=======

The text, images, contents, and source of the website are released under the
Creative Commons Attribution License 4.0.

Editing On Github
=================

Most editing to the site can be done via the Github website. Once the edits
have been merged into the master branch the website will build on Travis CI and
deploy automatically.

To edit and existing page, navigate to the ``.rst`` file you want to change in
the ``content`` directory and press the pencil button to edit the file. The
formatting should follow the rules of restructuredText (`example guide
<http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_). Once, done
submit a pull request and wait to see if the page properly builds without
errors and warnings. If it builds, then merge the pull request. If it fails,
then edit the files in the pull request to fix the errors and try again.

Local Build Instructions
========================

Install miniconda_, add the Conda Forge channel, and create an environment for
Pelican sites::

   $ conda config --add channels conda-forge
   $ conda create -n pelican python=3 pelican
   $ source activate pelican

Clone the plugin repository::

   (pelican)$ mkdir ~/src
   (pelican)$ git clone git@github.com:getpelican/pelican-plugins.git ~/src/pelican-plugins

Rebuild and serve the site locally::

   (pelican)$ make devserver

.. _miniconda: http://conda.pydata.org/miniconda.html

