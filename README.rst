packratt
========

``packratt`` is an application and a python package for downloading and
caching Radio Astronomy products, primarily to facilitate testing Radio
Astronomy software.

Installing
----------

For the lastest stable release

.. code:: bash

   $ pip install packratt

Usage
-----

Use an an linux application

.. code:: bash

   packratt get /ms/<telescope>/<observation_data>/<filename> <target_dir>
   packratt get /uvfits/<telescope>/<observation_date>/<filename> <target_dir>
   packratt get /beams/<telescope>/<filename> <target_dir>
   packratt get /gains/<telescope>/<observation_date>/<filename> <target_dir>

Use as a Python software package

.. code:: python

   import packratt

   packratt.get("/ms/<telescope>/<observation_data>/<filename>", target_dir)
   packratt.get("/uvfits/<telescope>/<observation_date>/<filename>", target_dir)
   packratt.get("/beams/<telescope>/<filename", target_dir)
   packratt.get("/gains/<telescope>/<observation_date>/<filename>", target_dir)

Registry schemas
~~~~~~~~~~~~~~~~

schemas are defined by a yaml registry file. E.g

.. code:: yaml

   '/test/ms/2020-06-04/google/smallest_ms.tar.gz':
     type: google
     file_id: 1wjZoh7OAIVEjYuTmg9dLAFiLoyehnIcL
     hash: 9d6379b5ad01a1fe6ec218d4e58e4620fa80ff9820f4f54bf185d86496f3456c
     description: >
       Small testing Measurement Set, stored on Google Drive

   '/test/ms/2020-06-04/elwood/smallest_ms.tar.gz':
     type: url
     url: ftp://elwood.ru.ac.za/pub/sjperkins/data/test/smallest_ms.tar.gz
     hash: 9d6379b5ad01a1fe6ec218d4e58e4620fa80ff9820f4f54bf185d86496f3456c
     description: >
       Small testing Measurement Set, stored on elwood's FTP server

Users can define their registry file and place them under
``$HOME/.config/packratt/registry.yaml``

Contributing
------------

To contribute, please adhere to
`pep8 <https://www.python.org/dev/peps/pep-0008/>`__ coding standards

License
-------

`LICENSE <LICENSE>`__
