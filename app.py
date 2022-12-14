from flask import Flask, session, request, render_template

app = Flask(__name__)
app.secret_key = '12345'


@app.route('/', methods=["POST", "GET"])
def home():
    if 'user' in session and len(session['user']):
        # user in session, we can change it or leave it as it is
        if request.method == "POST":
            if session['user'] == request.form['name'] or len(request.form['name']) == 0:
                # session not changed
                pass
            else:
                # new name, changing session
                session.permanent = True
                session.pop('user')
                session['user'] = request.form['name']
        return render_template("index.html", user=session['user'])
    else:
        # no user in session, we create a new one
        if request.method == "POST":
            if len(request.form['name']):
                # name inputted, we create a user
                session.permanent = True
                session['user'] = request.form['name']
                return render_template('index.html', user=session['user'])
            else:
                # empty input, no user
                return render_template("index.html", user='')
        else:
            # only for initial
            return render_template('index.html', user='')


if __name__ == '__main__':
    app.run(debug=True)
