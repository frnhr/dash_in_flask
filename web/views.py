from flask import render_template


__all__ = [
    "home_view",
    "page1_view",
    "page2_view",
]


def home_view():
    return render_template("pages/home.html")


def page1_view():
    return render_template("pages/page1.html")


def page2_view():
    return render_template("pages/page2.html")
