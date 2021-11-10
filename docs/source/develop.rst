Develop
=======

Installation Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 3.10
- Git

Setting Up the Environment
~~~~~

The development structure should should be two folders, the main folder DDRhythms contains all the code, while DDRhythms-Docs is used for deploying the docs to github pages.
If you do not intend to update the Docks then only DDRhythms is required.

Structure
----------
- DDRhythms
    - src
    - docs
    - tests
- DDRhythms-Docs
    - html

Steps
_____

.. code-block:: bash

    git clone https://github.com/Trafire/DDRhythms.git DDRhythms
    mkdir DDRhythms-Docs
    cd DDRhythms-Docs
    git clone https://github.com/Trafire/DDRhythms.git html
    git checkout -b gh-pages remotes/origin/gh-pages




