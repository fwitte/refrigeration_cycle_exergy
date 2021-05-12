Exergy Analysis of a Refrigeration Cycle in TESPy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Example for the exergy analysis in `TESPy <https://github.com/oemof/tespy>`_.
Find more information about the exergy analysis feature in the respective
`online documentation <https://tespy.readthedocs.io/>`_.

The refrigeration cycle model has the following topology:

.. figure:: ./flowsheet.svg
    :align: center
    :alt: Topology of the refrigeration cycle

Usage
-----
Clone the repository and build a new python environment. From the base
directory of the repository run

.. code-block:: bash

    pip install -r ./requirements.txt

to install the version requirements for the refrigeration.py python script.

The original data of the plant are obtained from the following publication:

*T. Morosuk, G. Tsatsaronis, Advanced exergoeconomic analysis of a
refrigeration machine: Part 1 — methodology and first evaluation, in: Energy
Systems Analysis, Thermodynamics and Sustainability Combustion Science and
Engineering Nanoengineering for Energy, Parts A and B, ASMEDC, 2011.
doi: 10.1115/imece2011-62688.*

Citation
--------
The state of this repository is archived via zenodo. If you are using the
TESPy model within your own research, you can refer to this model via the
zenodo doi: `10.5281/zenodo.TODO <https://zenodo.org/record/TODO>`_.

MIT License
-----------

Copyright (c) 2021 Francesco Witte, Julius Meier, Ilja Tuschy,
Mathias Hofmann

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
