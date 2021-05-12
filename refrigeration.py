# -*- coding: utf-8 -*-

from tespy.networks import Network
from tespy.components import (
    Sink, Source, Turbine, Condenser, HeatExchangerSimple, Merge, Splitter,
    Valve, HeatExchanger, CycleCloser, Compressor)
from tespy.connections import Connection, Bus, Ref
from tespy.tools import CharLine
from tespy.tools import document_model
import pandas as pd
import numpy as np
from tespy.tools import ExergyAnalysis

import plotly.graph_objects as go

from CoolProp.CoolProp import PropsSI as PSI


# specification of ambient state
pamb = 1
Tamb = 25


# setting up network
nw = Network(fluids=['Air', 'water'])
nw.set_attr(
    T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s',
    s_unit="kJ / kgK")

# components definition
water_in = Source('Water source')
water_out = Sink('Water sink')

air_in = Source('Air source')
air_out = Sink('Air sink')

closer = CycleCloser('Cycle closer')

cp = Compressor('Compressor')
turb = Turbine('Turbine')

cold = HeatExchanger('Cool side heat exchanger')
hot = HeatExchanger('Hot side heat exchanger')

# connections definition
# power cycle
c0 = Connection(cold, 'out2', closer, 'in1', label='0')
c1 = Connection(closer, 'out1', cp, 'in1', label='1')
c2 = Connection(cp, 'out1', hot, 'in1', label='2')
c3 = Connection(hot, 'out1', turb, 'in1', label='3')
c4 = Connection(turb, 'out1', cold, 'in2', label='4')

c11 = Connection(air_in, 'out1', cold, 'in1', label='11')
c12 = Connection(cold, 'out1', air_out, 'in1', label='12')

c21 = Connection(water_in, 'out1', hot, 'in2', label='21')
c22 = Connection(hot, 'out2', water_out, 'in1', label='22')

    # add connections to network
nw.add_conns(c0, c1, c2, c3, c4, c11, c12, c21, c22)

# power bus
power = Bus('power input')
power.add_comps(
    {'comp': turb, 'char': 1, 'base': 'component'},
    {'comp': cp, 'char': 1, 'base': 'bus'})

cool_product_bus = Bus('cooling')
cool_product_bus.add_comps(
    {'comp': air_in, 'base': 'bus'},
    {'comp': air_out})

heat_loss_bus = Bus('heat sink')
heat_loss_bus.add_comps(
    {'comp': water_in, 'base': 'bus'},
    {'comp': water_out})

nw.add_busses(power, cool_product_bus, heat_loss_bus)

# connection parameters
c0.set_attr(T=-30, p=1, fluid={'Air': 1, 'water': 0})
c2.set_attr(p=5.25)
c3.set_attr(p=5, T=35)
c4.set_attr(p=1.05)

c11.set_attr(fluid={'Air': 1, 'water': 0}, T=-10, p=1)
c12.set_attr(p=1, T=-20)


c21.set_attr(fluid={'Air': 0, 'water': 1}, T=25, p=1.5)
c22.set_attr(p=1.5, T=40)

# component parameters
turb.set_attr(eta_s=0.8)
cp.set_attr(eta_s=0.8)
cold.set_attr(Q=-100e3)

nw.solve(mode='design')

print(power.P.val / 0.9)
# Annahme, beide Wirkungsgrade sind gleich groß (P_ges * 0.9 geht in TESPy nicht)
eta = 0.961978
nw.del_busses(power)
power = Bus('power input')
power.add_comps(
    {'comp': turb, 'char': eta, 'base': 'component'},
    {'comp': cp, 'char': eta, 'base': 'bus'})
nw.add_busses(power)
nw.solve(mode='design')

# print results to prompt and generate model documentation
nw.print_results()
print(nw.results['Connection'])

dh1 = (nw.results['Connection'].loc['2', 'h'] - nw.results['Connection'].loc['1', 'h'])
dh2 = (nw.results['Connection'].loc['3', 'h'] - nw.results['Connection'].loc['2', 'h'])
dh3 = (nw.results['Connection'].loc['4', 'h'] - nw.results['Connection'].loc['3', 'h'])
dh4 = (nw.results['Connection'].loc['1', 'h'] - nw.results['Connection'].loc['4', 'h'])
dh5 = (nw.results['Connection'].loc['12', 'h'] - nw.results['Connection'].loc['11', 'h'])

dT1 = (nw.results['Connection'].loc['2', 'T'] - nw.results['Connection'].loc['1', 'T'])
dT2 = (nw.results['Connection'].loc['3', 'T'] - nw.results['Connection'].loc['2', 'T'])
dT3 = (nw.results['Connection'].loc['4', 'T'] - nw.results['Connection'].loc['3', 'T'])
dT4 = (nw.results['Connection'].loc['1', 'T'] - nw.results['Connection'].loc['4', 'T'])
dT5 = (nw.results['Connection'].loc['12', 'T'] - nw.results['Connection'].loc['11', 'T'])

print(dh1 / dT1)
print(dh2 / dT2)
print(dh3 / dT3)
print(dh4 / dT4)
print(dh5 / dT5)



document_model(nw)

# carry out exergy analysis
ean = ExergyAnalysis(nw, E_P=[cool_product_bus], E_F=[power], E_L=[heat_loss_bus])
ean.analyse(pamb=pamb, Tamb=Tamb)

for r in nw.results.values():
    print(r.dtypes)

# print exergy analysis results to prompt
ean.print_results()

print(ean.component_data)
print(ean.connection_data)
print(ean.bus_data)
print(ean.group_data)

ean.group_data[['E_F', 'E_P', 'E_D']] /= 1e3
ean.group_data[['epsilon', 'y_Dk', 'y*_Dk']] *= 1e2

# print(ean.group_data[['E_F', 'E_P', 'E_D', 'epsilon', 'y_Dk', 'y*_Dk']].to_latex(float_format='%.2f'))
# # generate Grassmann diagram
# links, nodes = ean.generate_plotly_sankey_input(display_thresold=1000)
#
# fig = go.Figure(go.Sankey(
#     arrangement="freeform",
#     node={
#         "label": nodes,
#         'pad': 11,
#         'color': 'orange'},
#     link=links))
# fig.show()
