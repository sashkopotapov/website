import request
from flask import Flask, render_template, request
from twitter_app import user_info
app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            name = request.form['username']
            user_info(name)
            return render_template('user.html')
        except:
            errors.append(
                "Try again"
            )
    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()