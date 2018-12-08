from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
import flask
from flask import Flask, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
from sqlalchemy import create_engine
from tests.config import app_config
import pandas as pd


def protect_views(app):
    for view_func in app.server.view_functions:
        if view_func.startswith(app.url_base_pathname):
            app.server.view_functions[view_func] = login_required(app.server.view_functions[view_func])
    return app


server = flask.Flask(__name__)

server.config.from_object(app_config['development'])
server.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)
engine = create_engine(server.config['SQLALCHEMY_DATABASE_URI'])

# flask-login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "login"


# user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = str(id)
        self.password = "secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20
users = [User("numpynewb")]


# somewhere to login
@server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == "secret":
            id = username
            user = User(id)
            login_user(user)
            return flask.redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@server.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@server.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)



dash_app1 = Dash(__name__, server=server, url_base_pathname='/dashboard/')
dash_app1.layout = html.Div([
    html.H1('Boudey-Org'),
    dcc.Tabs(id="tabs", value='tab-1-reminders', children=[
        dcc.Tab(label='Reminders', value='tab-1-reminders'),
        dcc.Tab(label='Other stuff', value='tab-2-else'),
    ]),
    html.Div(id='index')
])
@dash_app1.callback(Output('index', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    sticky = pd.read_sql('select id, completed, reminder, priority '
                         'from main.reminders_sticky '
                         'where username = "David Smith" order by priority desc',
                         engine)
    events = pd.read_sql('select id, completed_since_last, reminder, time_of_reminder, how_often '
                         'from main.reminders_events '
                         'where username = "David Smith"',
                         engine)

    if tab == 'tab-1-reminders':
        return html.Div([
            html.H3('Sticky Reminders'),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in sticky.columns],
                data=sticky.to_dict('rows'),
                style_cell={
                    'textAlign': 'left',
                    'minWidth': '0px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                },
                style_table= {
                    'overflowX': 'scroll'
                },
                style_data_conditional=[
                    {
                        'if': {
                            'filter': 'priority eq num(1)'
                        },
                        'backgroundColor': '#FF0000',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'filter': 'completed eq num(1)'
                        },
                        'backgroundColor': '#3D9970',
                        'color': 'white',
                    },
                ],
                css=[
                    {
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }
                ]
            ),
            html.H3('Event Reminders'),
            dash_table.DataTable(
                id='table2',
                columns=[{"name": i, "id": i} for i in events.columns],
                data=events.to_dict('rows'),
                style_cell={
                    'textAlign': 'left',
                    'minWidth': '0px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                },
                style_table={
                    'overflowX': 'scroll'
                },
                style_data_conditional=[
                    {
                        'if': {
                            'filter': 'completed_since_last eq num(1)'
                        },
                        'backgroundColor': '#3D9970',
                        'color': 'white',
                    },
                ],
                css=[
                    {
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }
                ]

            )
        ])
    elif tab == 'tab-2-else':
        return html.Div([
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

dash_app1 = protect_views(dash_app1)


@server.route('/')
@server.route('/index')
@login_required
def index():
    return 'hello world!'


@server.route('/dashboard')
def render_dashboard():
    return flask.redirect('/dash1')


app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server,
})

if __name__ == '__main__':
    run_simple('localhost', 5005, app, use_reloader=True, use_debugger=True)