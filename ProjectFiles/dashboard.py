from cmath import nan
from tempfile import SpooledTemporaryFile
import dash
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import utilities as ut
import numpy as np
import os
import re
"""  """
app = Dash(__name__)

colors = {
    'background': '#EEFFFF',
    'text': '#6F7080',
    'paper': '#E4F4FC'
}


list_of_subjects = []
subj_numbers = []
number_of_subjects = 0

folder_current = os.path.dirname(__file__) 
print(folder_current)
folder_input_data = os.path.join(folder_current, "input_data")
for file in os.listdir(folder_input_data):
    
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        print(file_name)
        list_of_subjects.append(ut.Subject(file_name))


df = list_of_subjects[0].subject_data


for i in range(number_of_subjects):
    subj_numbers.append(list_of_subjects[i].subject_id)

data_names = ["SpO2 (%)", "Blood Flow (ml/s)","Temp (C)"]
algorithm_names = ['min','max']
blood_flow_functions = ['CMA','SMA','Show Limits']


fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()
fig3= go.Figure()

fig0 = px.line(df, x="Time (s)", y = "SpO2 (%)")
fig1 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")
fig2 = px.line(df, x="Time (s)", y = "Temp (C)")
fig3 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")

app.layout = html.Div(children=[
    html.H1(children='Cardiopulmonary Bypass Dashboard', 
        style={
         'textAlign': 'center',
         'color': colors['text']
        } 
    ),

    html.Div(children='''
        Hier könnten Informationen zum Patienten stehen....
    '''),

    dcc.Checklist(
    id= 'checklist-algo',
    options=algorithm_names,
    inline=False
    ),

    html.Div([
        dcc.Dropdown(options = subj_numbers, placeholder='Select a subject', value='1', id='subject-dropdown'),
    html.Div(id='dd-output-container')
    ],
        style={"width": "15%"}
    ),

    dcc.Graph(
        id='dash-graph0',
        figure=fig0
    ),

    dcc.Graph(
        id='dash-graph1',
        figure=fig1
    ),
    dcc.Graph(
        id='dash-graph2',
        figure=fig2
    ),

    dcc.Checklist(
        id= 'checklist-bloodflow',
        options=blood_flow_functions,
        inline=False
    ),
    dcc.Graph(
        id='dash-graph3',
        figure=fig3
    )
])
### Callback Functions ###
## Graph Update Callback
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph0', 'figure'),
    Output('dash-graph1', 'figure'),
    Output('dash-graph2', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-algo','value')
)
def update_figure(value, algorithm_checkmarks):
    print("Current Subject: ",value)
    print("current checked checkmarks are: ", algorithm_checkmarks)
    ts = list_of_subjects[int(value)-1].subject_data
    #SpO2
    fig0 = px.line(ts, x="Time (s)", y = data_names[0])
    # Blood Flow
    fig1 = px.line(ts, x="Time (s)", y = data_names[1])
    # Blood Temperature
    fig2 = px.line(ts, x="Time (s)", y = data_names[2])
    
    ### Aufgabe 2: Min / Max ###

    grp = ts.agg(['max', 'min', 'idxmax', 'idxmin'])
    print(grp)

    fig0.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['paper'],
    font_color=colors['text']
    )

    fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['paper'],
    font_color=colors['text']
    )
    fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['paper'],
    font_color=colors['text']
    )

    if 'max' in algorithm_checkmarks:
        fig0.add_trace(go.Scatter(x = [grp.loc['idxmax', data_names[0]]], y = [grp.loc['max', data_names[0]]], 
                    mode ='markers', name= 'max', marker_symbol = 'star', marker_size = 15, marker_color = '#9B2533'))
        fig1.add_trace(go.Scatter(x = [grp.loc['idxmax', data_names[1]]], y = [grp.loc['max', data_names[1]]], 
                    mode ='markers', name= 'max', marker_symbol = 'star', marker_size = 15, marker_color = '#9B2533'))
        fig2.add_trace(go.Scatter(x = [grp.loc['idxmax', data_names[2]]], y = [grp.loc['max', data_names[2]]], 
                    mode ='markers', name= 'max', marker_symbol = 'star', marker_size = 15, marker_color = '#9B2533'))

    if 'min' in algorithm_checkmarks:
        fig0.add_trace(go.Scatter(x = [grp.loc['idxmin', data_names[0]]], y = [grp.loc['min', data_names[0]]], 
                    mode ='markers', name= 'min', marker_symbol = 'star', marker_size = 15, marker_color = '#05999B'))
        fig1.add_trace(go.Scatter(x = [grp.loc['idxmin', data_names[1]]], y = [grp.loc['min', data_names[1]]], 
                    mode ='markers', name= 'min', marker_symbol = 'star', marker_size = 15, marker_color = '#05999B'))
        fig2.add_trace(go.Scatter(x = [grp.loc['idxmin', data_names[2]]], y = [grp.loc['min', data_names[2]]], 
                    mode ='markers', name= 'min', marker_symbol = 'star', marker_size = 15, marker_color = '#05999B'))

    return fig0, fig1, fig2  


## Blodflow Simple Moving Average Update
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph3', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-bloodflow','value')
)
def bloodflow_figure(value, bloodflow_checkmarks):
    
    ## Calculate Moving Average: Aufgabe 2
    print(bloodflow_checkmarks)
    bf = list_of_subjects[int(value)-1].subject_data
    fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s)")
    
    
    if bloodflow_checkmarks == ["SMA"]:
        bf = list_of_subjects[int(value)-1].subject_data
        bf["Blood Flow (ml/s) - SMA"] = ut.calculate_SMA(bf["Blood Flow (ml/s)"],5) 
        fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s) - SMA")

    if bloodflow_checkmarks == ["CMA"]:
        bf = list_of_subjects[int(value)-1].subject_data
        bf["Blood Flow (ml/s) - CMA"] = ut.calculate_CMA(bf["Blood Flow (ml/s)"],2) 
        fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s) - CMA")

    #Durchschnitt
    avg = bf.mean()
    
    #Aufgabe 3-1, 3-2, 3-3 
    x = [0, 480]
    y = avg.loc['Blood Flow (ml/s)']
    y_oben = avg.loc['Blood Flow (ml/s)']*1.15
    y_unten = avg.loc['Blood Flow (ml/s)']*0.85

    if bloodflow_checkmarks == ["Show Limits"]:

        fig3.add_trace(go.Scatter(x = x, y= [y,y], mode = 'lines', name = 'average', line_color='#BFF172'))

        fig3.add_trace(go.Scatter(x = x, y = [y_oben,y_oben], mode = 'lines', name = 'upper line', line_color='#9B2533'))

        fig3.add_trace(go.Scatter(x = x, y = [y_unten, y_unten], mode = 'lines', name = 'under line', line_color='#05999B'))
        
    if bloodflow_checkmarks == ["SMA", "Show Limits"]:
        bf = list_of_subjects[int(value)-1].subject_data
        bf["Blood Flow (ml/s) - SMA"] = ut.calculate_SMA(bf["Blood Flow (ml/s)"],5) 
        fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s) - SMA")

        fig3.add_trace(go.Scatter(x = x, y= [y,y], mode = 'lines', name = 'average', line_color='#BFF172'))

        fig3.add_trace(go.Scatter(x = x, y = [y_oben,y_oben], mode = 'lines', name = 'upper line', line_color='#9B2533'))

        fig3.add_trace(go.Scatter(x = x, y = [y_unten, y_unten], mode = 'lines', name = 'under line', line_color='#05999B'))

    if bloodflow_checkmarks == ["CMA", "Show Limits"]:
        bf = list_of_subjects[int(value)-1].subject_data
        bf["Blood Flow (ml/s) - CMA"] = ut.calculate_CMA(bf["Blood Flow (ml/s)"],2) 
        fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s) - CMA")

        fig3.add_trace(go.Scatter(x = x, y= [y,y], mode = 'lines', name = 'average', line_color='#BFF172'))

        fig3.add_trace(go.Scatter(x = x, y = [y_oben,y_oben], mode = 'lines', name = 'upper line', line_color='#9B2533'))

        fig3.add_trace(go.Scatter(x = x, y = [y_unten, y_unten], mode = 'lines', name = 'under line', line_color='#05999B'))
    
   #if bloodflow_checkmarks == ["Show Limits"]:
        
        # uplimit= bf[(bf["Blood Flow (ml/s) - SMA"]>= y_oben)]
        # downlimit= bf[(bf["Blood Flow (ml/s) - SMA"]<= y_unten)]

        # beschreib = "values out of range:" + str(uplimit[bf["Blood Flow (ml/s) - SMA"]].count()) + str(downlimit[bf["Blood Flow (ml/s) - SMA"]].count()) +'s'
        
        # fig3.add_trace(go.Scatter(name= beschreib, x = uplimit['Time (s)'], y = uplimit, mode = 'markers', color = '#9B2533'))
        # fig3.add_trace(go.Scatter(name= beschreib, x = downlimit['Time (s)'], y = downlimit, mode = 'markers', color = '#05999B'))
    
    fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['paper'],
    font_color=colors['text']
    )


    return fig3

### Aufgabe 3.4 
# n = 5 ist optimale Lösung, falls n=3 Peaks ( von Störungen ) würden immer noch zu stark berücksichtigt und desto sichtbar. 
# Falls n > 5 dann die Kurve würde zu glad sein und desto die tatsächliche Werte zu stark vernichtet.
    
if __name__ == '__main__':
    app.run_server(debug=True)
