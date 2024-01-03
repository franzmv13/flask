
# from flask import Flask

# app = Flask(__name__)



# if __name__ == "__main__":
#     app.run(debug=True)



from flask import *
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "franz"
app.config["MYSQL_DB"] = "final"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/address", methods=["GET"])
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM final.address;""")
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)

@app.route("/address/<int:id>", methods=["GET"])
def get_actor_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM final.address WHERE `address_id` = {}""".format(id))
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)

@app.route("/address/<int:id>/agency", methods=["GET"])
def get_agency_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT address.country, agency.agency_name
                    FROM address
                    INNER JOIN agency on agency.id = address.address_id
                    WHERE agency.id = {};
                """.format(id))
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)



if __name__ == "__main__":
    app.run(debug=True)