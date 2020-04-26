import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import greport.loader as loader


def make_graph(pid):
    a = loader.get_data_object(pid)
    df = pd.read_csv("./media/Lab-Results-07112019.csv", header=0,
                     names=['PatientID', 'TestName', 'ParameterName', 'Result',
                            'ResultDatetime', 'Normal', 'ReferenceRange'])
    df = df.loc[df['PatientID'] == pid]
    df = df[df['ParameterName'] != 'Comment']
    df = df[df['Result'] != 'Subhead']
    df = df[df['Result'] != 'SubHead']
    df = df[pd.to_numeric(df['Result'], errors='coerce').notnull()]
    specs = [[{"type": "table"}]]
    row = len(a)+1
    titles = []
    for elem in a:
        specs.append([{"type": "bar"}])
        titles.insert(0, elem[1] + " on " + elem[0])
    titles.insert(0, "Test Results")
    fig = make_subplots(rows=row, cols=1, horizontal_spacing=0.3,
                        column_width=[500], specs=specs, subplot_titles=tuple(titles))
    df['TestName'] = df['TestName'] + df['ResultDatetime']
    for elem in df['TestName'].unique():
        temp = df.loc[df['TestName'] == elem]
        temp = temp.sort_values('Normal', ascending=False)
        color = []
        for ele in temp['Normal']:
            if ele == "N":
                color.append("green")
            elif ele == "H":
                color.append("red")
            else:
                color.append("blue")
        fig.add_trace(go.Bar(y=temp['ParameterName'], x=temp["Result"],
                             marker=dict(color=color),
                             width=.3, orientation="h",), row=row, col=1)
        row -= 1
    fig.add_trace(
        go.Table(header=dict(
                values=["TestName", "ParameterName", "Result", "ResultDatetime", "Normal", "ReferenceRange"],
                font=dict(size=10), align="left"),
            cells=dict(
                values=[df[k].tolist() for k in df.columns[1:]], align="left"),),
        row=1, col=1)
    fig.update_layout(height=4000, showlegend=False,
                      title_text="Graphical Report for patient : "+str(pid),)
    plotly.offline.plot(fig, filename='./templates/report.html', auto_open=False)


def make_trend(pid, testname):
    global title
    title = ""
    df = pd.read_csv("./media/Lab-Results-07112019.csv", header=0,
                     names=['PatientID', 'TestName', 'ParameterName', 'Result',
                            'ResultDatetime', 'Normal', 'ReferenceRange'])
    df = df.loc[df['PatientID'] == int(pid)]
    df = df.loc[df['TestName'] == testname]
    df = df[df['ParameterName'] != 'Comment']
    df = df[df['ParameterName'] != 'Comment:']
    df = df[df['Result'] != 'Subhead']
    df = df[df['Result'] != 'SubHead']
    df = df.sort_values('Normal', ascending=False)
    color = []
    for ele in df['Normal']:
        if ele == "N":
            color.append("green")
        elif ele == "H":
            color.append("red")
        else:
            color.append("blue")
    if len(df['ResultDatetime'].unique()) > 1:
        title += "Trend for "+testname
        data = []
        for elem in df['ResultDatetime'].unique():
            temp = df.loc[df['ResultDatetime'] == elem]
            data.append(
                    go.Bar(name=elem, x=temp['ParameterName'], y=temp['Result'],
                           text=temp['Result'], textposition='auto', width=0.3,
                           marker=dict(color=color),
                           ))
        fig = go.Figure(data=data)
        fig.update_layout(barmode='group')
    else:
        title += "Graph for "+testname+" on "+df['ResultDatetime'].unique()[0]
        dateandhour = df['ParameterName']
        values = df['Result']
        fig = go.Figure(data=[
            go.Bar(name='Present', x=dateandhour, y=values, text=values,
                   textposition='auto', width=0.3, marker=dict(color=color),)])
    fig.update_layout(
            title=title, xaxis_title="Parameters", yaxis_title="Values",
            font=dict(family="Courier New, monospace", size=24, color="#0f0f0f"))
    plotly.offline.plot(fig, filename='./templates/report.html', auto_open=False)
