from flask import Flask, render_template, request, redirect, jsonify
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'lead_gen_business')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leads/index_json')
def index_json():
    fullList = mysql.query_db("SELECT * FROM leads LIMIT 2, 5")
    return jsonify(fullList)

@app.route('/data/countrows', methods= ['POST', 'GET'])
def rowcount():
    query = "SELECT COUNT('id') AS 'all_rows' FROM leads WHERE first_name LIKE :name"
    data = {
        'name' : request.form['name'] + '%'
        }
    total_rows = mysql.query_db(query, data)
    print total_rows
    return jsonify(total_rows)

@app.route('/data/page/<page_num>/<rows_per_page>', methods= ['POST', 'GET'])
def pages(page_num, rows_per_page):
    total_rows = rows_per_page
    start = (int(page_num) - 1) * int(total_rows)
    query = "SELECT * FROM leads WHERE first_name LIKE :name LIMIT :near , :total_rows"
    data = {
        'name' : request.form['name'] + '%',
        'near' : start,
        'total_rows' : int(total_rows)
    }
    page_results = mysql.query_db(query, data)
    return jsonify(page_results)

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
