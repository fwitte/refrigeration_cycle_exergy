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

cold = HeatExchanger('Cooling heat exchanger')
hot = HeatExchanger('Heat sink heat exchanger')

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

# Assumption: both efficiency values are equal and sum up to a total of 10 %
# losses based on the resulting shaft power (direct implementation currently
# not possible in TESPy)
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

fmt = {
    'latex_body': True,
    'include_results': True,
    'HeatExchanger': {
        'params': ['Q', 'ttd_l', 'ttd_u', 'pr1', 'pr2']},
    'Connection': {
        'p': {'float_fmt': '{:,.4f}'},
        's': {'float_fmt': '{:,.4f}'},
        'h': {'float_fmt': '{:,.2f}'},
        'fluid': {'include_results': False}
    },
    'include_results': True,
    'draft': False
}
document_model(nw, fmt=fmt)

# carry out exergy analysis
ean = ExergyAnalysis(nw, E_P=[cool_product_bus], E_F=[power], E_L=[heat_loss_bus])
ean.analyse(pamb=pamb, Tamb=Tamb)

# print exergy analysis results to prompt
ean.print_results()

# generate Grassmann diagram
links, nodes = ean.generate_plotly_sankey_input(display_thresold=1000)

fig = go.Figure(go.Sankey(
    arrangement="freeform",
    node={
        "label": nodes,
        'pad': 11,
        'color': 'orange'},
    link=links))
fig.show()
