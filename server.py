from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.tpl")


@app.route('/login')
def service_login():
    return render_template("login.tpl")

@app.route('/register')
def service_register():
    return render_template("register.tpl")

@app.route('/challenges')
def service_chanllenges():
    return render_template("challenges.tpl")

@app.route('/users')
def service_usuarios():
    return render_template("users.tpl")

@app.route('/profile/<name>')
def service_dashboard(name):
    return render_template("profile.tpl")

@app.route('/challenge/<name>')
def service_challenge(name):
    return render_template("challenge.tpl")


@app.route('/upload/challenge')
def service_subchallenge():
    return render_template("subChallenge.tpl")

#@error(404)
#def error404(error):
#    return template("view/errors/404.tpl")
#
#@error(500)
#def error404(error):
#    return 'Nothing here, sorry 500'
#
#@error(505)
#def error404(error):
#    return 'Nothing here, sorry 505'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)