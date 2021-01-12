from .views import home_view, page1_view, page2_view


def bind_urls(app):
    app.route('/')(home_view)
    app.route('/page1/')(page1_view)
    app.route('/page2/')(page2_view)
