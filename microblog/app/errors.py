""" For error handing  """
from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    """ 
    Handle 404 error
    Args:
         error: Exception
     Returns:
         render_template('404.html'), 404: render 404.html template
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """ 
    Handle 500 error
    Args:
         error: Exception
     Returns:
         render_template('500.html'), 500: render 500.html template

    """
    db.session.rollback()
    return render_template('500.html'), 500
