import os
from flask import Flask, request, jsonify, render_template
from flaskext.mysql import MySQL
app = Flask(__name__)
mysqlconnector = MySQL()
# DB credentials
app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME', 'workers')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST', 'db')
mysqlconnector.init_app(app)

@app.route("/")
def index():
    return "Houdyyyy"

# TEST
@app.route("/test")
def health_check():
    return "healthy"
# ADD WORKER
@app.route("/addworker", methods=['POST'])
def addWorker():
    newWorker = request.get_json()    # GET INFO FROM THE CLIENT
    connection = mysqlconnector.connect()    # CONNCECT TO MYSQL
    cursor = connection.cursor()
    query = """ SELECT * FROM workers where id=%s """        # MAKE A QUERY
    cursor.execute(query, int(newWorker['id']))   #USE THE QUERY WITH THE ID ON THE DATABASE
    rows = cursor.fetchall()  #STORE IN ROWS
    if len(rows) > 0:      # CHECK IF USER EXSIST
        res = jsonify("Worker is already in the system")
        res.status_code = 400
    else:
        #IF USER NOT EXISTS
        # MAKE A QUERY
        query = """ INSERT into workers(firstname,lastname,age,id,email) values (%s,%s,%s,%s,%s) """
        # USE THE QUERY TO INSERT INFO TO newWorker
        cursor.execute(query, (newWorker['firstname'], newWorker['lastname'], newWorker['age'], newWorker['id'], newWorker['email']))
        connection.commit()   # COMMIT ON MYSQL
        res = jsonify("Added")
        res.status_code = 200
    cursor.close()    # CLOSE CONNECTION
    connection.close()
    return res

# ------ REMOVE WORKER --------
@app.route("/removeworker", methods=['DELETE'])
def removeWorker():
    deleteID = request.get_json()   # GET ID FROM THE CLIENT
    connection = mysqlconnector.connect()   # CONNCECT TO MYSQL
    cursor = connection.cursor()
    query = """ SELECT * FROM workers where id=%s """    # MAKE QUERY
    cursor.execute(query, int(deleteID['id']))   #GET WORKER WITH THIS ID
    rows = cursor.fetchall()     #STORE IN ROWS

# IF WORKER WITH THIS ID EXISTS
    if len(rows) > 0:
        query = """ DELETE FROM workers WHERE id=%s """   # MAKE QUERY
        cursor.execute(query, int(deleteID['id']))   #GET WORKER WITH THIS ID AND DELETE HIM
        connection.commit()    # COMMIT ON MYSQL
        res = jsonify("Remove sucsses")
        res.status_code = 200
# IF WORKER WITH THIS ID NOT EXISTS
    else:
        res = jsonify("Worker is Not found")
        res.status_code = 404
    cursor.close()    # CLOSE CONNECTION
    connection.close()
    return res


# ------SHOW ALL WORKERS ------
@app.route("/allworkers", methods=['GET'])
def allWorkers():
    connection = mysqlconnector.connect()   # CONNECT TO MYSQL
    cursor = connection.cursor()
    query = """ SELECT * FROM workers"""   # MAKE QUERY
    cursor.execute(query)   # COMMIT QUERY ON DATABASE
    rows = cursor.fetchall()   # GET FROM DATABASE AND STORE IN ROWS
    res = jsonify(rows)   # CONVORT ROWS TO JSON AND STORE IN RES
    res.status_code = 200
    cursor.close()   # CLOSE CONNECTION
    connection.close()
    return res

# -------SINGLE WORKER------
@app.route("/worker", methods=['GET'])
def worker():
    singleID = request.get_json()   # GET ID FROM THE CLIENT
    connection = mysqlconnector.connect()   # CONNECT TO MYSQL
    cursor = connection.cursor()
    query = """ SELECT * FROM workers where id=%s"""    # MAKE QUERY
    cursor.execute(query, int(singleID['id']))    #GET WORKER WITH THIS ID
    rows = cursor.fetchall()   # STORE IN ROWS
    res = jsonify(rows)    # CONVORT ROWS TO JSON AND STORE IN RES
    print(res)
    cursor.close()   # CLOSE CONNECTION
    connection.close()
    return res

# ------UPDATE WORKER ---------
@app.route("/updateworker", methods=['PUT'])
def updateWorker():
    updateWorker = request.get_json()  # GET ID FROM THE CLIENT
    connection = mysqlconnector.connect()  # CONNECT TO MYSQL
    cursor = connection.cursor()
    # CREATE QUERY
    query = """ UPDATE workers SET firstname = %s, lastname = %s, age = %s, id = %s, email = %s WHERE workerid = %s """
    # USE QEURY WITH THE INFO
    cursor.execute(query, [updateWorker["firstname"], updateWorker["lastname"], int(updateWorker["age"]), updateWorker['id'], updateWorker["email"], int(updateWorker["workerid"])])
    connection.commit()    # COMMIT ON DATABASE
    rows = cursor.fetchall()    # STORE IN ROWS
    print(rows)
    res = jsonify(rows)   # CONVERT ROWS TO JSON
    res.status_code = 200
    cursor.close()    # CLOSE CONNECTION
    connection.close()
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
