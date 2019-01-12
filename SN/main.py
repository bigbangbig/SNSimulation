import initialization.initialize as init
import plots.main as plots
import games.play as play
import games.update_network as update

import dash
import dash_core_components as dcc
import dash_html_components as html
import os

from dash.dependencies import Input
from flask import send_from_directory


app = dash.Dash()

fig = []
coop_plot = []
how_many_people = 500
cooperation_percentage = 30
rounds = 200
histories = 1
homophily = 1
position = 'r'
game = 'pd'
clusters = 1
network = 'new'
method = 'mu'
u1 = 4
u2 = 1
u3 = 2
u4 = 3

network_graph = init.go(how_many_people, cooperation_percentage, position, clusters)


def create():
    if network == "new":
        global network_graph
        network_graph = init.go(how_many_people, cooperation_percentage, position, clusters)
    else:
        init.assign_people_to_nodes(network_graph, cooperation_percentage, position)


def evolve(g):
    plots.init(g)
    plots.save_network_info(g, 0)

    # # بازی به تعداد مشخص شده در range بین همه گره ها انجام میشود
    for i in range(rounds):
        play.go(g, game, u1, u2, u3, u4)
        # update.copy_fittest(G)
        update.conditional_update(g, homophily, method)
        plots.save_network_info(g, i + 1)
    global fig, coop_plot
    fig, coop_plot = plots.show_results(g, network)


evolve(network_graph)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div(children=[
    html.Link(
        rel='stylesheet',
        href='/dash_files/site.css'
    ),
    html.H1(children='تحلیل چگونگی فراگیر شدن تمکین به قانون در جوامع'),
    html.Hr(),
    # __________________________________________________________
    # اطلاعات شبکه، تعداد نودها و استراتژی اولیه نودهای مرکزی
    html.Div(children=[
        html.H3(id='hi', children=['اطلاعات جامعه']),
        html.Div(id='network-info', children=fig[1])],
        className="section"),
    html.Div(children=[
        html.H3("مقادیر انتخاب شده"),
        html.Span('گره ها (تعداد افراد جامعه): '),
        html.Strong(html.Span(id='node-count-value',
                    children=how_many_people)),
        html.Br(),
        html.Span('درصد تمکین کنندگان در آغاز فرایند: '),
        html.Strong(html.Span(id='cooperators-value',
                    children=cooperation_percentage)),
        html.Span('%'),
        html.Br(),
        html.Span('تعداد دورهای انجام تعامل: '),
        html.Strong(html.Span(id='rounds-value',
                    children=rounds)),
        html.Br(),
        html.Span('سطح یکریختی جامعه: '),
        html.Strong(html.Span(id='homophily-value',
                    children=homophily)),
        html.Br(),
        html.Span('تعداد بخش های جامعه: '),
        html.Strong(html.Span(id='clusters-value',
                    children=clusters)),
        html.Br(),
        html.Span('تکامل برای '),
        html.Strong(children=html.Span(id='hist-value',
                    children=histories)),
        html.Span(" مرتبه، تکرار شود."),
        html.Br(),
        html.Button('آغاز تکامل', id='go', className='button',
                    style={"vertical-align": "middle"}),
        dcc.Input(id='signal',
                  type='text',
                  value='',
                  style={'display': 'none'}),
    ], className='section'),
    # اجرای شبیه سازی
    # _______________________________________
    html.Div(children=[
        html.H3("تنظیم مقادیر"),
        # تعداد نودها
        dcc.Slider(
            id='node-count',
            min=50,
            max=1000,
            step=50,
            value=200,
            updatemode='drag',
            className="slider"
        ),
        # درصد همکاری کنندگان
        dcc.Slider(
            id='cooperators',
            min=1,
            max=100,
            step=1,
            value=10,
            updatemode='drag',
            className="slider"
        ),
        # تعداد دورهای بازی
        dcc.Slider(
            id="rounds",
            min=50,
            max=500,
            step=50,
            value=200,
            updatemode='drag',
            className="slider"
        ),
        # سطح هموفیلی گره ها
        dcc.Slider(
            id="homophily",
            min=1,
            max=8,
            step=1,
            value=2,
            updatemode='drag',
            className="slider"
        ),
        # تعداد کلاسترها
        dcc.Slider(
            id="cluster",
            min=1,
            max=5,
            step=1,
            value=1,
            updatemode='drag',
            className="slider"
        ),
        # تعداد تکرار آزمایش
        dcc.Slider(
            id="hist",
            min=1,
            max=20,
            step=1,
            value=histories,
            updatemode='drag',
            className="slider"
        ),
        # موقعیت همکاری کنندگان
        dcc.RadioItems(
            id='position',
            options=[
                {'label': 'تصادفی', 'value': 'r'},
                {'label': 'مرکزی', 'value': 'c'},
                {'label': 'لبه', 'value': 'e'}
            ],
            value=position,
            className='slider radios'
        ),
        # بازی
        dcc.RadioItems(
            id='game',
            options=[
                {'label': "معمای زندانی", 'value': 'pd'},
                {'label': 'شاهین ها و کبوترها', 'value': 'sd'},
                {'label': 'تنظیم عایدی ها به صورت دلخواه', 'value': 'custom'}
            ],
            value=game,
            className='slider radios'
        ),
        # نحوه تغییر استراتژی
        dcc.RadioItems(
            id='update_method',
            options=[
                {'label': "همسایه تصادفی", 'value': 'rd'},
                {'label': 'همسایه دارای بیشترین عایدی', 'value': 'mu'}
            ],
            value=method,
            className='slider radios'
        ),
        # شبکه
        dcc.RadioItems(
            id='new-network',
            options=[
                {'label': "جامعه جدید", 'value': 'new'},
                {'label': 'همین جامعه', 'value': 'same'}
            ],
            value=network,
            className='slider radios'
        )], className='section'),
    html.Div(id="utilities",
             children=[
                 html.Div(children=[
                            # عایدی ها
                            dcc.Slider(
                                id="u1",
                                min=1,
                                max=10,
                                step=1,
                                value=u1,
                                updatemode='drag',
                                className="slider"
                            ),
                            dcc.Slider(
                                id="u2",
                                min=1,
                                max=10,
                                step=1,
                                value=u2,
                                updatemode='drag',
                                className="slider"
                            ),
                            dcc.Slider(
                                id="u3",
                                min=1,
                                max=10,
                                step=1,
                                value=u3,
                                updatemode='drag',
                                className="slider"
                            ),
                            dcc.Slider(
                                id="u4",
                                min=1,
                                max=10,
                                step=1,
                                value=u4,
                                updatemode='drag',
                                className="slider"
                            )
                 ], className='graph-section'),
                 html.Div(children=[
                     html.Table(
                         [
                             html.Tr([html.Th(""), html.Th("تمکین"), html.Th("تمرد")])
                         ] +
                         [
                             html.Tr([html.Td("تمکین"),
                                      html.Td(html.Span(id='u1-value',
                                                        children=str(u4) + "," + str(u4))),
                                      html.Td(html.Span(id='u2-value',
                                                        children=str(u2) + "," + str(u1)))]),
                             html.Tr([html.Td("تمرد"),
                                      html.Td(html.Span(id='u3-value',
                                                        children=str(u1) + "," + str(u2))),
                                      html.Td(html.Span(id='u4-value',
                                                        children=str(u3) + "," + str(u3)))])
                         ]
                     ),
                 ], className="section")
                ],),
    html.Hr(style={'width': '100%'}, className='graph-section'),
    # _______________________________________________________
    # گراف شبکه در نسل آخر
    html.Div(children=[
        html.H3(children='''
                            شبکه، گره ها و ارتباطات بین آن ها                
                '''),
        dcc.Graph(
            id='graph',
            figure=fig[0]
            )
    ], className='graph-section'),
    # نمودار تغییر تعداد همکاری کنندگان در طول نسلها
    html.Div(children=[
        html.H3('تعداد تمکین کنندگان در هر مرحله'),
        dcc.Graph(
            id='plot',
            figure=coop_plot
        )
    ], className="graph-section"),
])


@app.callback(dash.dependencies.Output('signal', 'value'),
              [dash.dependencies.Input('go', 'n_clicks')])
def signal(n_clicks):
    if not n_clicks == 0 and n_clicks is not None:
        global network
        create()
        evolve(network_graph)
        temp = network
        network = "old"
        if histories > 1:
            for i in range(histories):
                create()
                evolve(network_graph)
        network = temp
    return n_clicks


@app.callback(dash.dependencies.Output('plot', 'figure'),
              [dash.dependencies.Input('signal', 'value')])
def plot(value):
    return coop_plot


@app.callback(dash.dependencies.Output('graph', 'figure'),
              [dash.dependencies.Input('signal', 'value')])
def graph(value):
    return fig[0]


@app.callback(dash.dependencies.Output('network-info', 'children'),
              [dash.dependencies.Input('signal', 'value')])
def info(value):
    return fig[1]


@app.callback(dash.dependencies.Output('node-count-value', 'children'),
              [dash.dependencies.Input('node-count', 'value')])
def change_count(value):
    global how_many_people
    how_many_people = value
    return value


@app.callback(dash.dependencies.Output('hist-value', 'children'),
              [dash.dependencies.Input('hist', 'value')])
def change_count(value):
    global histories
    histories = value
    return value


@app.callback(dash.dependencies.Output('node-count', 'disabled'),
              [dash.dependencies.Input('new-network', 'value')])
def change_count(value):
    if value == "new":
        return False
    else:
        return True


@app.callback(dash.dependencies.Output('cluster', 'disabled'),
              [dash.dependencies.Input('new-network', 'value')])
def change_count(value):
    if value == "new":
        return False
    else:
        return True


@app.callback(dash.dependencies.Output('cooperators-value', 'children'),
              [dash.dependencies.Input('cooperators', 'value')])
def change_count(value):
    global cooperation_percentage
    cooperation_percentage = value
    return value


@app.callback(dash.dependencies.Output('rounds-value', 'children'),
              [dash.dependencies.Input('rounds', 'value')])
def change_count(value):
    global rounds
    rounds = value
    return value


@app.callback(dash.dependencies.Output('homophily-value', 'children'),
              [dash.dependencies.Input('homophily', 'value')])
def change_count(value):
    global homophily
    homophily = value
    return value


@app.callback(dash.dependencies.Output('clusters-value', 'children'),
              [dash.dependencies.Input('cluster', 'value')])
def change_count(value):
    global clusters
    clusters = value
    return value


@app.callback(dash.dependencies.Output('position', 'className'),
              [dash.dependencies.Input('position', 'value')])
def change_count(value):
    global position
    position = value
    return "slider radios"


@app.callback(dash.dependencies.Output('game', 'className'),
              [dash.dependencies.Input('game', 'value')])
def change_count(value):
    global game
    game = value
    return "slider radios"


@app.callback(dash.dependencies.Output('utilities', 'className'),
              [dash.dependencies.Input('game', 'value')])
def change_count(value):
    global game
    if not value == "custom":
        global u1, u2, u3, u4
        if value == 'pd':
            u1 = 4
            u2 = 1
            u3 = 2
            u4 = 3
        elif value == 'sd':
            u1 = 4
            u2 = 2
            u3 = 1
            u4 = 3
        return "visible"
    else:
        return ""


@app.callback(dash.dependencies.Output('u1-value', 'children'),
              [dash.dependencies.Input('u4', 'value')])
def change_count(value):
    global u4
    u4 = value
    return str(u4) + " , " + str(u4)


@app.callback(dash.dependencies.Output('u4-value', 'children'),
              [dash.dependencies.Input('u3', 'value')])
def change_count(value):
    global u3
    u3 = value
    return str(u3) + " , " + str(u3)


@app.callback(dash.dependencies.Output('u2-value', 'children'),
              [dash.dependencies.Input('u2', 'value'),
               dash.dependencies.Input('u1', 'value')])
def change_count(u2value, u1value):
    global u2, u1
    u1 = u1value
    u2 = u2value
    return str(u2) + " , " + str(u1)


@app.callback(dash.dependencies.Output('u3-value', 'children'),
              [dash.dependencies.Input('u2', 'value'),
               dash.dependencies.Input('u1', 'value')])
def change_count(u2value, u1value):
    global u2, u1
    u1 = u1value
    u2 = u2value
    return str(u1) + " , " + str(u2)


@app.callback(dash.dependencies.Output('update_method', 'className'),
              [dash.dependencies.Input('update_method', 'value')])
def change_count(value):
    global method
    method = value
    return "slider radios"


@app.callback(dash.dependencies.Output('new-network', 'className'),
              [dash.dependencies.Input('new-network', 'value')])
def change_count(value):
    global network
    network = value
    return "slider radios"


@app.server.route('/dash_files/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'dash_files')
    return send_from_directory(static_folder, path)


if __name__ == '__main__':
    app.run_server(debug=False)
    print("hi")

app = dash.Dash(__name__)

server = app.server

