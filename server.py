#!/usr/bin/python3

from flask import render_template
import connexion

tp = connexion.App(__name__, specification_dir='./')
tp.add_api('swagger.yml')


@tp.route('/')
def home():
    """
    Respond to localhost:5000 request with home.html

    :return: rendered home.html
    """
    return render_template('home.html')


if __name__ == '__main__':
    tp.run(port=5000, debug=True)
