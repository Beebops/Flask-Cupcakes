from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# the toolbar is only enabled in debug mode:
app.debug = True
app.config['SECRET_KEY'] = 'shhhsecret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns json of all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)



if __name__ == "__main__":
    app.run(debug=True)