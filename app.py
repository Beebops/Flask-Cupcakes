from flask import Flask, jsonify, request, render_template, redirect, flash
from flask_cors import CORS
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
CORS(app, methods=['GET', 'POST', 'DELETE'])
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///cupcakes_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# the toolbar is only enabled in debug mode:
app.debug = True
app.config['SECRET_KEY'] = 'shhhsecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

@app.route('/')
def show_cupcakes():
    """Renders html template with a list of all cupcakes"""
    #cupcakes = Cupcake.query.all()
    return render_template('index.html')

@app.route("/api/cupcakes")
def list_cupcakes():
    """Returns json of all cupcakes resources
    """
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Returns json of a single cupcake resource"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add a new cupcake resource to db"""
    data = request.json
    new_cupcake = Cupcake(
        flavor=data["flavor"],
        size=data["size"],
        rating=data["rating"],
        image=data["image"] or None
    )
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Updates a cupcake resource"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Remove cupcake resource from db"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")


if __name__ == "__main__":
    app.run(debug=True)
