Develop
=======

Installation Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 3.10
- Git

Setting Up the Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

The development structure should should be two folders, the main folder DDRhythms contains all the code, while DDRhythms-Docs is used for deploying the docs to github pages.
If you do not intend to update the Docs then only DDRhythms is required.

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

    Set up Repos

.. code-block:: bash

    git clone https://github.com/Trafire/DDRhythms.git DDRhythms
    mkdir DDRhythms-Docs
    cd DDRhythms-Docs
    git clone https://github.com/Trafire/DDRhythms.git html
    git checkout -b gh-pages remotes/origin/gh-pages

Set Up Virtual Environment
__________________________

.. code-block:: bash

    cd ../DDRhythms
    pip3 install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pre-commit install

Update Docs
~~~~~~~~~~~
In the main repo
-----------------
    currently only working on windows


    - edit and commit code as usual
    - make any changes required in docs and docs/sources
    - document stuff in README.rst, commit it as usual
    - make github