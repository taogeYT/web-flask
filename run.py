# -*- coding: utf-8 -*-
"""
app startup entry
"""
__author__ = "lyt"

from app import create_app

if __name__ == "__main__":
    app = create_app('default')
    app.run(debug=True)
