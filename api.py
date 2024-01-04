
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

@app.route("/patients", methods=["GET"])
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM final.patients;""")
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)

@app.route("/patients/<int:id>", methods=["GET"])
def get_actor_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM final.patients WHERE `id` = {}""".format(id))
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)

@app.route("/patients/<int:id>/agency", methods=["GET"])
def get_agency_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT patients.first_name,patients.last_name, agency.agency_name
                    FROM patients
                    INNER JOIN agency on agency.id = patients.id
                    WHERE agency.id = 2 {};
                """.format(id))
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)


@app.route("/patients", methods=["POST"])
def add_actor():
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstname = info["fname"]
    lastname = info["lname"]
    print(firstname , lastname)
    cur.execute(
        """ INSERT INTO `final`.`patients` (`first_name`, `last_name`) VALUES (%s, %s)""",
        (firstname, lastname),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "patients added successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/patients/<int:id>", methods=["PUT"])
def update_patients(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstname = info["fname"]
    lastname = info["lname"]
    cur.execute(
        """UPDATE `final`.`patients` SET `first_name` = %s, `last_name` = %s WHERE (`id` = %s);
 """,
        (firstname, lastname, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "patients updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/patients/<int:id>", methods=["DELETE"])
def del_patients(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM patients where id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "patients deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
if __name__ == "__main__":
    app.run(debug=True)