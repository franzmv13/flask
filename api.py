
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

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

@app.route("/", methods=["GET"])
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM final.address;""")
    rv = cur.fetchall()
    return make_response(jsonify(rv), 200)

if __name__ == "__main__":
    app.run(debug=True)