from flask import Flask

import web.urls
from dash1.dashapp import DashApp1
from dash2.dashapp import DashApp2

application = Flask(__name__)
web.urls.bind_urls(application)
DashApp1.register(application)
DashApp2.register(application)


if __name__ == "__main__":
    application.run(debug=True)
