Introduction
============

This Product extracts latitude and longitude out of the EXIF_ informations
of an Image and sets its coordinates to them. The placemark marker is
set to the images thumbnail. It extracts the information when an
image is added or you can call it manually by appending
`/@@extract_exif_geoannotations.html` to its url. You may also mass
annotate all contents of a folder or an entire site by calling this
view on a folder or the site root.

Installation
============

This addon can be installed has any other addons, please follow official
documentation_.

.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to

The short version is:
++++++++++++++++++++++

Add ``collective.geo.exif`` to the list of eggs to install, e.g.

::

    [buildout]
    ...
    eggs =
        ...
        collective.geo.exif

Re-run buildout, e.g. with

::

    $ ./bin/buildout

Restart Plone.

.. _EXIF: http://www.exif.org/
