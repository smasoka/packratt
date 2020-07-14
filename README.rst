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

   packratt ....

Use as a Python software package

.. code:: python

   import packratt

   packratt.get("")
   packratt.get("")
   packratt.get("") 

Registry schemas
~~~~~~~~~~~~~~~~

schemas are defined by a yaml registry file

.. code:: yaml

Users can define their registry file and place them under
``/home/username/.packratt/registry.yaml``

Contributing
------------

To contribute, please adhere to
`pep8 <https://www.python.org/dev/peps/pep-0008/>`__ coding standards

License
-------

`LICENSE <LICENSE>`__
