import initialization.initialize as init
import plots.main as plots
import games.play as play
import games.update_network as update

import dash
import dash_core_components as dcc
import dash_html_components as html
import os

from dash.dependencies import Input, Output
from flask import send_from_directory


app = dash.Dash()

fig = []
coop_plot = []
how_many_people = 500
cooperation_percentage = 30
rounds = 200
homophily = 1
position = 'r'
game = 'pd'


def evolve():
    #  اطلاعات اولیه گراف را ذخیره میکند. مثل تعداد گره ها
    graph = init.go(how_many_people, cooperation_percentage, position)
    plots.init(graph)
    plots.save_network_info(graph, 0)

    # # بازی به تعداد مشخص شده در range بین همه گره ها انجام میشود
    for i in range(rounds):
        play.go(graph, game)
        # update.copy_fittest(G)
        update.conditional_update(graph, homophily)
        plots.save_network_info(graph, i + 1)
    global fig, coop_plot
    fig, coop_plot = plots.show_results(graph)


evolve()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div(children=[
    html.Link(
        rel='stylesheet',
        href='/dash_files/site.css'
    ),
    html.H1(children='Analysing Human Cooperation Patterns'),
    html.Hr(),
    # _______________________________________________________
    # گراف شبکه در نسل آخر
    html.Div(children=[
        html.H3(children='''
                The Network, nodes and connections between them
                '''),
        dcc.Graph(
            id='graph',
            figure=fig[0]
            )
    ], className='graph-section'),
    # نمودار تغییر تعداد همکاری کنندگان در طول نسلها
    html.Div(children=[
        html.H3('Number of cooperators in each generation/round'),
        dcc.Graph(
            id='plot',
            figure=coop_plot
        )
    ], className="graph-section"),
    html.Hr(),
    # __________________________________________________________
    # اطلاعات شبکه، تعداد نودها و استراتژی اولیه نودهای مرکزی
    html.Div(children=[
        html.H3(id='hi', children=['Network information']),
        html.Div(id='network-info', children=fig[1])],
        className="section"),
    html.Div(children=[
        html.H3("Selected settings"),
        html.Span('Nodes (the number of people): '),
        html.Span(id='node-count-value',
                  children=how_many_people),
        html.Br(),
        html.Span('Cooperators percentage at the beginning: '),
        html.Span(id='cooperators-value',
                  children=cooperation_percentage),
        html.Span('%'),
        html.Br(),
        html.Span('Rounds to be played (number of generations): '),
        html.Span(id='rounds-value',
                  children=rounds),
        html.Br(),
        html.Span('Homophily level: '),
        html.Span(id='homophily-value',
                  children=homophily),
        html.Br(),
        html.Button('Start the Evolution', id='go', className='button',
                    style={"vertical-align": "middle"}),
        dcc.Input(id='signal',
                  type='text',
                  value='',
                  style={'display': 'none'}),
    ], className='section'),
    # اجرای شبیه سازی
    # _______________________________________
    html.Div(children=[
        html.H3("Configure the simulation"),
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
        # موقعیت همکاری کنندگان
        dcc.RadioItems(
            id='position',
            options=[
                {'label': 'Random', 'value': 'r'},
                {'label': 'Central', 'value': 'c'},
                {'label': 'Edge', 'value': 'e'}
            ],
            value=position,
            className='slider radios'
        ),
        # بازی
        dcc.RadioItems(
            id='game',
            options=[
                {'label': "Prisoner's Dilemma", 'value': 'pd'},
                {'label': 'Snow Drift', 'value': 'sd'}
            ],
            value=game,
            className='slider radios'
        )], className='section'),
])


@app.callback(dash.dependencies.Output('signal', 'value'),
              [dash.dependencies.Input('go', 'n_clicks')])
def signal(n_clicks):
    if not n_clicks == 0 and n_clicks is not None:
        evolve()
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


@app.server.route('/dash_files/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'dash_files')
    return send_from_directory(static_folder, path)


if __name__ == '__main__':
    app.run_server(debug=True)


