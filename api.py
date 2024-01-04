
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

@app.route("/manager", methods=["GET"])
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM final.manager;""")
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)

@app.route("/manager/<int:id>", methods=["GET"])
def get_actor_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM final.manager WHERE `id` = {}""".format(id))
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)

@app.route("/manager/<int:id>/agency", methods=["GET"])
def get_agency_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT manager.first_name,manager.last_name, agency.agency_name
                    FROM manager
                    INNER JOIN agency on agency.id = manager.id
                    WHERE agency.id = 2 {};
                """.format(id))
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)


@app.route("/manager", methods=["POST"])
def add_actor():
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstname = info["fname"]
    lastname = info["lname"]
    print(firstname , lastname)
    cur.execute(
        """ INSERT INTO `final`.`manager` (`first_name`, `last_name`) VALUES (%s, %s)""",
        (firstname, lastname),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "manager added successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/manager/<int:id>", methods=["PUT"])
def update_actor(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstname = info["fname"]
    lastname = info["lname"]
    cur.execute(
        """UPDATE `final`.`manager` SET `first_name` = %s, `last_name` = %s WHERE (`id` = %s);
 """,
        (firstname, lastname, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)