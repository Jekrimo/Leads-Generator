from flask import Flask, render_template, request, redirect, jsonify
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'lead_gen_business')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leads/search', methods= ["POST"])
def search():
     query = "SELECT * FROM leads WHERE first_name LIKE :name OR registered_datetime BETWEEN :start_date AND :end_date"
     data = {
         'name' : request.form['name'] + '%',
         'start_date' : request.form['from_date'],
         'end_date' : request.form['to_date']
      }
     fullList = mysql.query_db(query, data)
     #  fullList = mysql.query_db("SELECT * FROM leads")
     return render_template('partials/leads.html', fullList = fullList)
      #SELECT * FROM leads WHERE name = :name AND date = :date;

if __name__ == "__main__":
    app.run(port=5000, debug=True)
