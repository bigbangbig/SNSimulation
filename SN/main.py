import initialization.initialize as init
import plots.main as plots
import games.play as play
import games.update_network as update

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import os
from flask import send_from_directory

#  اطلاعات اولیه گراف را ذخیره میکند. مثل تعداد گره ها
G = init.go(500, 30)
plots.init(G)
plots.save_network_info(G, 0)

# # بازی به تعداد مشخص شده در range بین همه گره ها انجام میشود
for i in range(200):
    play.go(G)
    # update.copy_fittest(G)
    update.conditional_update(G)
    plots.save_network_info(G, i + 1)

fig, annotation = plots.show_results(G)

app = dash.Dash()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div(children=[
    html.Link(
        rel='stylesheet',
        href='/dash_files/site.css'
    ),
    html.H1(children='Analysing Human Cooperation Patterns'),

    html.H3(children='''
        The Network, nodes and connections between them
    '''),
    html.Div(annotation),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


@app.server.route('/dash_files/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'dash_files')
    return send_from_directory(static_folder, path)


if __name__ == '__main__':
    app.run_server(debug=True)


