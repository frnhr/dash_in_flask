from flask import Flask

import web.urls
from dash1.dashapp import DashApp1
from dash2.dashapp import DashApp2

app = Flask(__name__)
web.urls.bind_urls(app)
DashApp1.register(app)
DashApp2.register(app)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
