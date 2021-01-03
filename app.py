from flask import Flask, render_template, redirect
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_app

mars_coll = db.mars

@app.route('/')
def index():

    mars_data = mars_coll.find_one()

    return(render_template('index.html', mars_data=mars_data))

@app.route('/scrape')
def scrape():

    import scrape_mars

    nasa_document = scrape_mars.scrape_all()

    mars_coll.update_one({}, {'$set': nasa_document}, upsert=True)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)