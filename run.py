# -*- coding: utf-8 -*-
"""
app startup entry
"""
__author__ = "lyt"

from app import create_app

if __name__ == "__main__":
    env = 'default'
    app = create_app(env)
    app.run(host='0.0.0.0', debug=True)
