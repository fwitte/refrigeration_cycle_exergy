# Exergy Analysis of a Refrigeration Cycle in TESPy

Example for the exergy analysis in [TESPy][]. Find more information
about the exergy analysis feature in the respective [online
documentation][].

The refrigeration cycle model has the following topology:

<figure>
<img src="./flowsheet.svg" class="align-center" />
</figure>

## Usage

Clone the repository and build a new python environment. From the base
directory of the repository run

``` bash
pip install -r ./requirements.txt
```

to install the version requirements for the refrigeration.py python
script.

The original data of the plant are obtained from the following
publication:

*T. Morosuk, G. Tsatsaronis, Advanced exergoeconomic analysis of a
refrigeration machine: Part 1 — methodology and first evaluation, in:
Energy Systems Analysis, Thermodynamics and Sustainability Combustion
Science and Engineering Nanoengineering for Energy, Parts A and B,
ASMEDC, 2011. doi: 10.1115/imece2011-62688.*

## Valdiation and Results of Exergy Analysis

The tables below show the results of the simulation as well as the
validation results. The original data from the publication are provided
in the .csv files [component_validation.csv][] and
[connection_validation.csv][].

### Connection data

**TESPy simulation**

|    |   e_PH in kJ/kg |   e_T in kJ/kg |   e_M in kJ/kg |   E_PH in kW |   E_T in kW |   E_M in kW |
|:---|----------------:|---------------:|---------------:|-------------:|------------:|------------:|
| 0  |             5.8 |            5.8 |            0.0 |        23.98 |       23.98 |        0.00 |
| 1  |             5.8 |            5.8 |            0.0 |        23.98 |       23.98 |        0.00 |
| 2  |           163.9 |           22.1 |          141.8 |       674.08 |       90.85 |      583.23 |
| 3  |           137.8 |            0.2 |          137.6 |       566.77 |        0.68 |      566.09 |
| 4  |            17.1 |           12.9 |            4.2 |        70.28 |       53.11 |       17.17 |
| 11 |             2.2 |            2.2 |            0.0 |        22.31 |       22.31 |        0.00 |
| 12 |             3.8 |            3.8 |            0.0 |        37.82 |       37.82 |        0.00 |
| 21 |             0.1 |           -0.0 |            0.1 |         0.40 |       -0.00 |        0.40 |
| 22 |             1.6 |            1.5 |            0.1 |        12.47 |       12.07 |        0.40 |

**Absolute difference in the values Δ**

|    |   Δ m in kg/s |   Δ T in °C |   Δ p in bar |   Δ h in kJ/kg |   Δ e_T in kJ/kg |   Δ e_M in kJ/kg |
|:---|--------------:|------------:|-------------:|---------------:|-----------------:|-----------------:|
| 1  |        -0.085 |         0.0 |         0.00 |            0.0 |              0.0 |              0.0 |
| 2  |        -0.085 |         0.2 |         0.00 |            0.1 |              0.0 |             -0.0 |
| 3  |        -0.085 |        -0.0 |        -0.00 |           -0.7 |              0.0 |             -0.0 |
| 4  |        -0.085 |        -0.4 |         0.00 |           -0.5 |              0.0 |              0.0 |
| 11 |        -0.023 |         0.0 |         0.00 |            0.1 |              0.0 |              0.0 |
| 12 |        -0.023 |         0.0 |         0.00 |            0.1 |              0.0 |              0.0 |
| 21 |        -0.106 |         0.0 |         0.00 |            0.0 |             -0.0 |              0.0 |
| 22 |        -0.106 |         0.0 |         0.00 |           -0.0 |             -0.0 |              0.0 |

**Relative deviation in the values δ**

|    |   δ m in % |   δ T in % |   δ p in % |   δ h in % |   δ e_T in % |   δ e_M in % |
|:---|-----------:|-----------:|-----------:|-----------:|-------------:|-------------:|
| 1  |     -2.024 |       -0.0 |        0.0 |        nan |          0.2 |          nan |
| 2  |     -2.024 |        0.1 |        0.0 |        0.0 |          0.5 |         -0.1 |
| 3  |     -2.024 |       -0.0 |       -0.0 |       -1.0 |         10.7 |         -0.0 |
| 4  |     -2.024 |        0.7 |        0.0 |        2.2 |          1.4 |          0.1 |
| 11 |     -0.229 |       -0.0 |        0.0 |        0.6 |          0.2 |          nan |
| 12 |     -0.229 |       -0.0 |        0.0 |        0.6 |          0.1 |          nan |
| 21 |     -1.328 |        0.0 |        0.0 |        nan |         -inf |          0.3 |
| 22 |     -1.328 |        0.0 |        0.0 |       -0.0 |         -0.3 |          0.3 |

*Deviation due to differences in fluid property data*

### Component data

**TESPy simulation**

|                          |   E_F in kW |   E_P in kW |   E_D in kW |   ε in % |   y_Dk in % |   y*_Dk in % |
|:-------------------------|------------:|------------:|------------:|---------:|------------:|-------------:|
| Cooling heat exchanger   |       46.30 |       15.51 |       30.79 |     33.5 |         7.0 |          7.5 |
| Compressor               |      815.29 |      674.08 |      141.21 |     82.7 |        32.1 |         34.3 |
| Heat sink heat exchanger |      107.31 |       12.07 |       95.24 |     11.2 |        21.7 |         23.1 |
| Turbine                  |      549.60 |      404.62 |      144.98 |     73.6 |        33.0 |         35.2 |

**Disaggregating the Inverter from the Compressor and Turbine**

|                          |   E_F in kW |   E_P in kW |   E_D in kW |
|:-------------------------|------------:|------------:|------------:|
| Compressor               |      785.21 |      674.08 |      111.12 |
| Cooling heat exchanger   |       46.30 |       15.51 |       30.79 |
| Heat sink heat exchanger |      107.31 |       12.07 |       95.24 |
| Inverter                 |      439.80 |      395.82 |       43.98 |
| Turbine                  |      549.60 |      418.51 |      131.09 |

**Absolute difference in the values Δ compared to disaggregation**

|                          |   Δ E_F in kW |   Δ E_P in kW |   Δ E_D in kW |
|:-------------------------|--------------:|--------------:|--------------:|
| Compressor               |        -15.99 |        -13.82 |         -2.18 |
| Cooling heat exchanger   |         -0.26 |         -0.00 |         -0.26 |
| Heat sink heat exchanger |         -1.79 |         -0.17 |         -1.62 |
| Inverter                 |         -7.76 |         -6.98 |         -0.78 |
| Turbine                  |        -11.60 |         -8.79 |         -2.81 |

**Relative deviation in the values δ compared to disaggregation**

|                          |   δ E_F in % |   δ E_P in % |   δ E_D in % |
|:-------------------------|-------------:|-------------:|-------------:|
| Compressor               |        -2.00 |        -2.01 |        -1.92 |
| Cooling heat exchanger   |        -0.56 |        -0.00 |        -0.84 |
| Heat sink heat exchanger |        -1.64 |        -1.40 |        -1.67 |
| Inverter                 |        -1.73 |        -1.73 |        -1.74 |
| Turbine                  |        -2.07 |        -2.06 |        -2.10 |

*High deviation due to differences in component exergy balances*

### Network data (results only)

|   E_F in kW |   E_P in kW |   E_D in kW |   E_L in kW |   ε in % |
|------------:|------------:|------------:|------------:|---------:|
|      439.80 |       15.51 |      412.23 |       12.07 |      3.5 |

## Citation

The state of this repository is archived via zenodo. If you are using the
TESPy model within your own research, you can refer to this model via the
zenodo doi: [10.5281/zenodo.4751856][].

## MIT License

Copyright (c) Francesco Witte, Julius Meier, Ilja Tuschy, Mathias Hofmann

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

  [TESPy]: https://github.com/oemof/tespy
  [online documentation]: https://tespy.readthedocs.io/
  [pdf model report]: refrigeration_model_report.pdf
  [component_validation.csv]: component_validation.csv
  [connection_validation.csv]: connection_validation.csv
  [10.5281/zenodo.4751856]: https://zenodo.org/record/4751856
