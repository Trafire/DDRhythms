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

    - edit and commit code as usual
    - document stuff in README.rst, commit it as usual
    - document stuff that will be in the documentation, but not on the main page, in other .rst files in the docs directory.
    - change to docs dir and run make html to generate the html docs in your docs repo. This should not make any changes to the main repo, so you don’t have to commit again
    - if you’re making a PDF manual, make that too with make latexpdf. Depending on where you’re putting the PDF manual, you’ll have to commit and push the new version as well.
    - git push
    - change to the docs repo

In the Docs repo
----------------
    - change to the docs repo (make sure you’re in the html dir)
    - check to make sure you’re on the gh-pages branch
    - commit
    - push
    - enjoy




