
csv_zip_rsync
=============


.. image:: https://img.shields.io/pypi/v/package_name.svg
   :target: https://pypi.python.org/pypi/csv_zip_rsync
   :alt: Latest PyPI version


compress csv to zip and rsync to remote server

Usage
-----

Installation
------------

Used compression method
-----------------------

.. code-block::

   Original File :5902183
   ZIP_STORED :zip_stats.st_size=5902297 rate:100.00% time:0.02641892433166504
   ZIP_DEFLATED :zip_stats.st_size=1280575 rate:21.70% time:1.8873212337493896
   ZIP_BZIP2 :zip_stats.st_size=1093927 rate:18.53% time:0.8491525650024414
   ZIP_LZMA :zip_stats.st_size=972919 rate:16.48% time:5.862420558929443

``LZMA`` showed most efficient compression rate. ``LIP_BZIP2`` was fast enough. so I chose BZIP2.

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

package_name was written by `fx-kirin <fx.kirin@gmail.com>`_.
