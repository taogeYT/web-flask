# from flask import Flask, session, redirect, url_for, escape, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     if 'username' in session:
#         # import pdb
#         # pdb.set_trace()
#         print(session['username'])
#         return 'Logged in as %s' % escape(session['username'])
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     app.logger.debug('A value for debugging')
#     app.logger.warning('A warning occurred (%d apples)', 42)
#     app.logger.error('An error occurred')
#     if request.method == 'POST':
#         # session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form action="" method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))

# # set the secret key.  keep this really secret:
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# app.logger.error('An error occurred')
# app.run(debug=True)
