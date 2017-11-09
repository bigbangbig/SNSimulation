import networkx as nx
import matplotlib.pyplot as plt
import plotly as py
from plotly.graph_objs import *

# متغیرهای عمومی برای ذخیره اطلاعات
cooperators_in_round = []
node_count = 0


# رسم نمودار تعداد همکاری کنندگان بر حسب دورهای بازی
def plot():
    x = [x[0] for x in cooperators_in_round]
    y = [x[1] for x in cooperators_in_round]
    trace = Scatter(
        x=x,
        y=y,
        mode='lines'
    )
    data = [trace]
    py.offline.plot(data, filename='Images/Cooperators.html')


# شماره دور بازی و گراف شبکه را به صورت ورودی دریافت می کند
def save_network_info(network, game_round):
    cooperators = 0
    # تعداد همکاری کنندگان را محاسبه کرده
    for i in network.nodes:
        if network.nodes[i]['personality'].strategy == "C":
            cooperators += 1
    global cooperators_in_round
    # و این تعداد را به همراه شماره دور کنونی در یک لیست ذخیره می کند
    cooperators_in_round.append((game_round, cooperators))


# اطلاعات شبکه اولیه را ذخیره میکند
def init(network):
    global node_count
    node_count = len(network.nodes)


# DEPRECATED
# گراف شبکه را به عنوان ورودی دریافت کرده آن را رسم میکند
def show_network(g):
    # برای هر گره استراتژی و برازندگی هر یک از گره ها محاسبه شده
    # و به صورت برچسب در هر گره نمایش داده میشود
    # for v in g.nodes():
    #     g.node[v]['state'] = str(v.fitness) + v.strategy

    # for v in g.nodes():
    bb = nx.eigenvector_centrality(g)
    nx.set_node_attributes(g, bb, 'state')

    pos = nx.spring_layout(g)

    plt.figure(figsize=(12, 8))
    nx.draw(g, pos)
    node_labels = nx.get_node_attributes(g, 'state')
    nx.draw_networkx_labels(g, pos, labels=node_labels)

    # edge_labels = nx.get_edge_attributes(g, 'state')
    # nx.draw_networkx_edge_labels(g, pos, labels=edge_labels)
    plt.savefig('Images/Network.png')
    plt.show()


def draw(g):
    pos = nx.fruchterman_reingold_layout(g)
    N = node_count
    Xv = [pos[k][0] for k in range(N)]
    Yv = [pos[k][1] for k in range(N)]
    Xed = []
    Yed = []
    for edge in g.edges():
       Xed += [pos[edge[0]][0],pos[edge[1]][0], None]
       Yed += [pos[edge[0]][1],pos[edge[1]][1], None]
    width = 1500
    height = 800
    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )
    layout = Layout(title="The Network, nodes and connections between them",
                    font=Font(size=12),
                    showlegend=False,
                    autosize=False,
                    width=width,
                    height=height,
                    xaxis=XAxis(axis),
                    yaxis=YAxis(axis),
                    margin=Margin(
                        l=40,
                        r=40,
                        b=85,
                        t=100,
                    ),
                    hovermode='closest',
                    annotations=Annotations([
                        Annotation(
                            showarrow=False,
                            text='This igraph.Graph has the Kamada-Kawai layout',
                            xref='paper',
                            yref='paper',
                            x=0,
                            y=-0.1,
                            xanchor='left',
                            yanchor='bottom',
                            font=Font(
                                size=14
                            )
                        )
                    ]),
                    )

    edge_trace = Scatter(x=Xed,
                         y=Yed,
                         mode='lines',
                         line=Line(color='rgb(210,210,210)', width=1),
                         hoverinfo='none'
                         )

    # ایجاد برچسب برای هر یک از گره ها
    labels = []

    # برچسب استراتژی
    personalities = nx.get_node_attributes(g, 'personality')
    for i in personalities:
        labels.append("Strategy: " + str(personalities[i].strategy))

    # برچسب مقدار مرکزیت بردار ویژه
    # در صورت رخ دادن exception تا 10 بار محاسبه مجددا انجام میشود
    while True:
        counter = 0;
        try:
            if counter > 10:
                break
            bb = nx.eigenvector_centrality(g)

            nx.set_node_attributes(g, bb, 'state')
            centrality_values = nx.get_node_attributes(g, 'state')
            for i in centrality_values:
                labels[i] += ("<br>Centrality: " + str(centrality_values[i]))

        except nx.exception.PowerIterationFailedConvergence:
            continue
        break
        counter += 1

    node_trace = Scatter(x=Xv,
                         y=Yv,
                         mode='markers',
                         name='net',
                         marker=Marker(symbol='dot',
                                       size=15,
                                       colorscale='YIOrRd',
                                       reversescale=True,
                                       color=[],
                                       colorbar=dict(
                                           thickness=15,
                                           title='Node Centrality',
                                           xanchor='left',
                                           titleside='right'
                                       ),
                                       line=Line(color='rgb(50,50,50)', width=0.5)
                                       ),
                         text=labels,
                         hoverinfo='text'
                         )

    for node in g.nodes():
        node_trace['marker']['color'].append(g.nodes[node]['state'])

    annot = "Number of nodes: " + str(node_count) + "<br>" +\
            "Cooperators in last round: " + str(cooperators_in_round[-1][1])

    data1 = Data([edge_trace, node_trace])
    fig1 = Figure(data=data1, layout=layout)
    fig1['layout']['annotations'][0]['text'] = annot
    py.offline.plot(fig1, filename='Images/Network.html')

#     todo for annotations, title and each plot's config go to documentation: https://plot.ly/python/subplots/


def show_results(g):
    draw(g)
    plot()
