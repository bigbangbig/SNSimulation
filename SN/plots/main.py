import networkx as nx
import matplotlib.pyplot as plt
from plotly.graph_objs import *
import operator
import dash_html_components as html

# متغیرهای عمومی برای ذخیره اطلاعات
cooperators_in_round = []
node_count = 0
centrality_values = []
children = []
xv = []
yv = []
xed = []
yed = []
data = []


# رسم نمودار تعداد همکاری کنندگان بر حسب دورهای بازی
def plot(network):
    x = [x[0] for x in cooperators_in_round]
    y = [x[1] for x in cooperators_in_round]
    global data
    if network == "new":
        data = []

    trace = Scatter(
        x=x,
        y=y,
        mode='lines',
        name=str(len(data) + 1)
    )

    data.append(trace)
    figure = Figure(
        data=data
    )

    if not network == "new":
        av_y = []
        counter = 0
        for i in range(len(x)):
            av_y.append(0)
            for j in data:
                av_y[counter] += j.y[i]
            av_y[counter] /= len(data)
            # for j in i.y:
            #     # print(j)
            #     av_y[counter] += i.y[j]
            # av_y[counter] / len(i.y)
            counter += 1
        av_trace = Scatter(
            y=av_y,
            x=x,
            mode='markers',
            name='Average'
        )

        if len(data) > 2:
            data[0] = av_trace
        else:
            data.insert(0, av_trace)

    return figure


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

    global cooperators_in_round
    cooperators_in_round = []

    global centrality_values
    centrality_values = nx.get_node_attributes(network, 'state')

    sorted_centralities = reversed(sorted(centrality_values.items(), key=operator.itemgetter(1)))

    centrality_counter = 1
    global children
    children = [
        "Strategies of the most central nodes at the beginning: ",
        html.Br()]
    for (node, centrality) in sorted_centralities:
        if centrality_counter > 10:
            break
        children.append(html.Span("(" + str(centrality_counter) + "). Centrality: " + '%.5f' % centrality +
                                  ", Strategy: " + network.nodes[node]['personality'].strategy))
        children.append(html.Br())
        centrality_counter += 1


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


def draw(g, network):
    # pos = nx.fruchterman_reingold_layout(g)
    # pos = nx.spring_layout(g, iterations=1000, dim=3)
    global xv, yv, xed, yed
    if network == 'new':
        pos = nx.spring_layout(g)
        n = node_count
        xv = [pos[k][0] for k in range(n)]
        yv = [pos[k][1] for k in range(n)]
        # zv = [pos[k][2] for k in range(n)]
        xed = []
        yed = []
        # zed = []
        for edge in g.edges():
            xed += [pos[edge[0]][0], pos[edge[1]][0], None]
            yed += [pos[edge[0]][1], pos[edge[1]][1], None]
            # zed += [pos[edge[0]][2], pos[edge[1]][2], None]

    axis = dict(showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )
    layout = Layout(font=Font(size=12),
                    showlegend=False,
                    autosize=True,
                    xaxis=XAxis(axis),
                    yaxis=YAxis(axis),
                    margin=Margin(
                        l=40,
                        r=40,
                        b=0,
                        t=0,
                    ),
                    hovermode='closest'
                    )

    edge_trace = Scatter(x=xed,
                         y=yed,
                         # z=zed,
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
    global centrality_values
    for i in centrality_values:
        labels[i] += ("<br>Centrality: " + str(centrality_values[i]))

    node_trace = Scatter(x=xv,
                         y=yv,
                         # z=zv,
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

    annotation = html.Div(children=[html.Span(children=children)])

    data1 = Data([edge_trace, node_trace])
    fig1 = Figure(data=data1, layout=layout)
    # fig1['layout']['annotations'][0]['text'] = annotation
    # py.offline.plot(fig1, filename='Images/Network.html')
    # return Figure(data=data1), annotation
    return fig1, annotation


def show_results(g, network):
    figure = draw(g, network)
    coop_plot = plot(network)
    return figure, coop_plot
