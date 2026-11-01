from flask import render_template
from . import app, db

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    return render_template("500.html"), 500

@app.errorhandler(505)
def error_505(error):
    return render_template("505.html"), 505

