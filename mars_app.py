from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# Create an instance of Flask
app = Flask(__name__)

# The default port used by MongoDB is 27017
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# Create route that renders index.html template and finds data from mongo
@app.route("/")
def home(): 
    # Find data
    mars_facts = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_facts)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
