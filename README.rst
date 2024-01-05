============
In-Struct-Me
============

.. contents::
   :depth: 2
   :backlinks: none

Introduction
------------

This tool recursively searches for C structs in a user-chosen folder. It then
creates a Graphviz dot file, which, in turn, generates an image showing how
different C structs are interlinked.

This script can be helpful when trying to learn a new codebase, as often just
looking at the structs can provide a good understanding of what the code is
trying to accomplish.

Note: Currently, it only searches for "struct", therefore typedef'd structs
won't be found.

Installation
------------

Requirements that needs to be installed (apt, dnf, ...)

.. code:: bash

   graphviz
   python3
   build-essential

1. Clone the code:

   .. code:: bash

      git@github.com:jbech-linaro/in-struct-me.git

Usage
-----

Once installed, here's how you can use In-Struct-Me:

1. Generate the dot file and PNG for the example code.

   .. code:: bash

      make

2. Same as "1", but make it verbose.

   .. code:: bash

      make V=1

3. Same as "1", but grep for "foo".

   .. code:: bash

      make G=foo

4. Scan another folder (can be combined with parameter as already shown)

   .. code:: bash

      make F=~/linux_kernel/drivers/tee

  or to scan multiple folders

   .. code:: bash

      make F="~/linux_kernel/drivers/tee ~/another/folder"

5. Use another Graphviz tool (``neato``, ``circo``, ``twopi``, ``fdp``) instead
   of the default ``dot``.

   .. code:: bash

      make T=circo

6. Use another ignore file than the default

   .. code:: bash

      make I=another-ignore-file.txt

7. Generate a PNG with a user specified name

   .. code:: bash

      make O=another-name.png

Configuration
-------------

If you encounter many nodes that aren't of interest, you can add text to the
``ignore.txt`` file. Everything added there will be removed from the generated
graph and image.

Examples
--------

Here are some examples to help you get started:

- Structure relations in the Linux kernel OP-TEE folder

  .. code:: bash

    make F=~/devel/linux/drivers/tee/optee

  .. image:: images/example1.png
    :width: 800px
    :align: center

- Same as above, but grep for ``shm``

  .. code:: bash

    make F=~/devel/linux/drivers/tee/optee G=shm

  .. image:: images/example2.png
    :width: 800px
    :align: center

- Same as above, but also show verbose

  .. code:: bash

    make F=~/devel/linux/drivers/tee/optee G=shm V=1

  .. image:: images/example3.png
    :width: 800px
    :align: center


FAQ
---

1. **Why are some nodes squares and others circles?**

   Squares represent structs with complete definitions under the specified path.
   These structs may contain other structs not found under the path. Represented
   as circles, a link is created due to a lack of information about their
   definitions.

2. **Why does grep sometimes find things that I cannot see?**

   This occurs when not using the verbose option. However, the script
   recognizes that this struct includes a variable matching your grep criteria,
   hence it is displayed.

3. **Things seems to crash?**

   Most likely you have chosen a folder that contains too much data. Try to
   limit the amount of c and h files exposed to the script.

4. **Things are missing in the image?**

   The ``ignore.txt`` in this git contains a few words already. See if what you
   are looking for is in that file. If it is, just remove it and save the file
   and re-run the script.
