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



fmt_dict = {
    'E_F': {
        'unit': ' in kW',
        'float': '{:.2f}',
        'factor': 1e3,
    },
    'E_P': {
        'unit': ' in kW',
        'float': '{:.2f}',
        'factor': 1e3,
    },
    'E_D': {
        'unit': ' in kW',
        'float': '{:.2f}',
        'factor': 1e3,
    },
    'E_L': {
        'unit': ' in kW',
        'float': '{:.2f}',
        'factor': 1e3,
    },
    'epsilon': {
        'unit': ' in %',
        'float': '{:.1f}',
        'factor': 1 / 100,
        'markdown_header': 'ε'
    },
    'y_Dk': {
        'unit': ' in %',
        'float': '{:.1f}',
        'factor': 1 / 100
    },
    'y*_Dk': {
        'unit': ' in %',
        'float': '{:.1f}',
        'factor': 1 / 100
    },
    'e_T': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1000
    },
    'e_M': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1000
    },
    'e_PH': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1000
    },
    'E_T': {
        'unit': ' in kW',
        'float': '{:.2f}',
        'factor': 1e3
    },
    'E_M': {
        'unit': ' in kW',
        'float': '{:.2f}',
        'factor': 1e3
    },
    'E_PH': {
        'unit': ' in kW',
        'float': '{:.2f}',
        'factor': 1e3
    },
    'T': {
        'unit': ' in °C',
        'float': '{:.1f}',
        'factor': 1
    },
    'p': {
        'unit': ' in bar',
        'float': '{:.2f}',
        'factor': 1
    },
    'h': {
        'unit': ' in kJ/kg',
        'float': '{:.1f}',
        'factor': 1
    },
    'm': {
        'unit': ' in kg/s',
        'float': '{:.3f}',
        'factor': 1
    }
}


def result_to_markdown(df, filename, prefix=''):

    for col in df.columns:
        fmt = fmt_dict[col]['float']
        if prefix == 'δ ':
            unit = ' in %'
            df[col] *= 100
        else:
            unit = fmt_dict[col]['unit']
            df[col] /= fmt_dict[col]['factor']
        for row in df.index:
            df.loc[row, col] = str(fmt.format(df.loc[row, col]))
        if 'markdown_header' not in fmt_dict[col]:
            fmt_dict[col]['markdown_header'] = col

        df = df.rename(columns={
            col: prefix + fmt_dict[col]['markdown_header'] + unit
        })
    df.to_markdown(
        filename, disable_numparse=True,
        colalign=['left'] + ['right' for _ in df.columns]
    )


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

# norm values to to E_F
links['value'] = [val / links['value'][0] for val in links['value']]

fig = go.Figure(go.Sankey(
    arrangement="snap",
    textfont={"family": "Linux Libertine O"},
    node={
        "label": nodes,
        'pad': 11,
        'color': 'orange'},
    link=links))
fig.show()

# validation (connections)

df_original_data = pd.read_csv(
    'connection_validation.csv', sep=';', decimal=',', index_col='label'
)

df_tespy = pd.concat(
    # units of exergy are J/kg in TESPy, kJ/kg in original data
    [nw.results['Connection'], ean.connection_data / 1e3], axis=1
)
# zero point of enthalpy is different than in original data
# using connection 1 and 21 as reference
air_idx = [1, 2, 3, 4, 11, 12]
water_idx = [21, 22]
# make index numeric to match indices
df_tespy.index = pd.to_numeric(df_tespy.index, errors='coerce')
df_tespy.loc[air_idx, 'h'] = (
    df_tespy.loc[air_idx, 'h'] - df_tespy.loc[air_idx[0], 'h']
)
df_tespy.loc[water_idx, 'h'] = (
    df_tespy.loc[water_idx, 'h'] - df_tespy.loc[water_idx[0], 'h']
)
# same for original data
df_original_data.loc[air_idx, 'h'] = (
    df_original_data.loc[air_idx, 'h'] - df_original_data.loc[air_idx[0], 'h']
)
df_original_data.loc[water_idx, 'h'] = (
    df_original_data.loc[water_idx, 'h'] - df_original_data.loc[water_idx[0], 'h']
)

# make index numeric to match indices
df_tespy.index = pd.to_numeric(df_tespy.index, errors='coerce')
# select available indices
idx = np.intersect1d(df_tespy.index, df_original_data.index)
df_tespy = df_tespy.loc[idx, df_original_data.columns]

df_diff_abs = df_tespy - df_original_data
df_diff_rel = (df_tespy - df_original_data) / df_original_data

result_to_markdown(df_diff_abs, 'connections_delta_absolute', 'Δ ')
result_to_markdown(df_diff_rel, 'connections_delta_relative', 'δ ')

# validation (components, needs re-check)

df_original_data = pd.read_csv(
    'component_validation.csv', sep=';', decimal=',', index_col='label'
)

# use aggregated data, as these include mechanical losses of compressor/turbine
df_tespy = ean.component_data.copy()
df_tespy.loc['Inverter', 'E_D'] = ean.bus_data.loc[['Turbine', 'Compressor'], 'E_D'].sum()
df_tespy.loc['Inverter', 'E_P'] = ean.bus_data.loc['Compressor', 'E_P'] - ean.bus_data.loc['Turbine', 'E_F']
df_tespy.loc['Inverter', 'E_F'] = df_tespy.loc['Inverter', 'E_P'] + df_tespy.loc['Inverter', 'E_D']
# # select available indices
idx = np.intersect1d(df_tespy.index, df_original_data.index)
cols = ['E_F', 'E_P', 'E_D']
# original data in kW
df_tespy = df_tespy.loc[idx, cols] / 1e3
df_original_data = df_original_data.loc[idx, cols]

df_diff_abs = (df_tespy - df_original_data).dropna()
df_diff_rel = ((df_tespy - df_original_data) / df_original_data).dropna()

result_to_markdown(df_diff_abs * 1e3, 'components_delta_absolute', 'Δ ')
result_to_markdown(df_diff_rel, 'components_delta_relative', 'δ ')

# export results

network_result = ean.network_data.to_frame().transpose()

ean.aggregation_data.drop(columns=['group'], inplace=True)
result_to_markdown(ean.aggregation_data, 'components_result')
result_to_markdown(ean.connection_data, 'connections_result')
result_to_markdown(network_result, 'network_result')
