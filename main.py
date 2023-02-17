from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras


# Create a Flask Instance
app = Flask(__name__)
# Database Connection


def database():
    connection = psycopg2.connect.connect(user="postgres",
                                          password="password",
                                          host="192.168.1.43",
                                          port="5432",
                                          database="hospitalmanagement")
    cursor = connection.cursor()

# database güncellendi
# Create a route decorator


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # sqlite
        with psycopg2.connect(user="postgres",
                              password="password",
                              host="192.168.1.43",
                              port="5432",
                              database="hospitalmanagement") as connection:
            cursor = connection.cursor()
        # htmlform
        panelemail = request.form['panelemail']
        panelpassword = request.form['panelpassword']
        # query
        query = "SELECT doctoremail, doctorpassword FROM doctors where doctoremail= '" + \
            panelemail+"' and doctorpassword='"+panelpassword+"'"
        cursor.execute(query)

        results = cursor.fetchall()
        # validation
        if len(results) == 0:
            print("Sorry, Incorrect Credentials Porvided. Try Again!")
        else:
            return render_template("loggedin.html")
    return render_template('index.html')


@app.route('/createnewdoctor')
def createnewdoctor():
    return render_template('createnewdoctor.html')

# database güncellemesi yapıldı


@app.route('/shownewdoctor', methods=['POST', 'GET'])
def shownewdoctor():
    if request.method == 'POST':
        try:
            doctoridnumber = request.form['doctoridnumber']
            doctorfirstname = request.form['doctorfirstname']
            doctorlastname = request.form['doctorlastname']
            doctorpassword = request.form['doctorpassword']
            doctorspeciality = request.form['doctorspeciality']
            doctorworkingshift = request.form['doctorworkingshift']
            doctorphonenumber = request.form['doctorphonenumber']
            doctoremailaddress = request.form['doctoremailaddress']

            connection = psycopg2.connect(user="postgres",
                                          password="password",
                                          host="192.168.1.43",
                                          port="5432",
                                          database="hospitalmanagement")

            cursor = connection.cursor()

            postgres_insert_doctors = """INSERT INTO doctors (doctorid, doctorname, doctorsurname, doctorpassword, doctorspeciality,doctorshift, doctorphone, doctoremail)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

            doctorrecord_to_insert = (doctoridnumber, doctorfirstname, doctorlastname, doctorpassword,
                                      doctorspeciality, doctorworkingshift, doctorphonenumber, doctoremailaddress)

            cursor.execute(postgres_insert_doctors, doctorrecord_to_insert)

            connection.commit()
            doctorcount = cursor.rowcount
            msg = doctorcount, "Record inserted successfully into doctors table"
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into doctors table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                return render_template("shownewdoctor.html", msg=msg)
                connection.close()


@ app.route('/addpatient')
def projects():
    return render_template('addpatient.html')

# database güncellendi


@ app.route('/showaddedpatient', methods=['POST', 'GET'])
def showaddedpatient():

    if request.method == 'POST':
        try:
            idnumber = request.form['idnumber']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            placeofbirth = request.form['placeofbirth']
            dateofbirth = request.form['dateofbirth']
            gender = request.form['gender']
            joindate = request.form['joindate']
            phonenumber = request.form['phonenumber']
            emailaddress = request.form['emailaddress']
            address = request.form['address']

            connection = psycopg2.connect(user="postgres",
                                          password="password",
                                          host="192.168.1.43",
                                          port="5432",
                                          database="hospitalmanagement")

            cursor = connection.cursor()

            postgres_insert_patients = """INSERT INTO patients (patientid, patientname, patientsurname, pplaceofbirth, pdateofbirth, pgender, pdateofjoin, patientnumber, patientemail, patientadress) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            patientrecord_to_insert = (idnumber, firstname, lastname, placeofbirth,
                                       dateofbirth, gender, joindate, phonenumber, emailaddress, address)

            cursor.execute(postgres_insert_patients, patientrecord_to_insert)
            connection.commit()
            patientcount = cursor.rowcount
            msg = (patientcount, "Record inserted successfully into patients table")
        except (Exception, psycopg2.Error) as error:
            msg = ("Failed to insert record into doctors table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
            return render_template("showaddedpatient.html", msg=msg)
            connection.close()

# database güncellendi


@ app.route('/patientlist')
def list():
    connection = psycopg2.connect(user="postgres",
                                  password="password",
                                  host="192.168.1.43",
                                  port="5432",
                                  database="hospitalmanagement")

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = f"""
    SELECT * FROM patients
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template("patientlist.html", rows=rows)


@ app.route('/deletepatient')
def deletelistwithrowid():
    connection = psycopg2.connect(user="postgres",
                                  password="password",
                                  host="192.168.1.43",
                                  port="5432",
                                  database="hospitalmanagement")
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = f"""
    SELECT * FROM patients
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template("deletepatient.html", rows=rows)


@ app.route('/shownewpatientlistafterdelete', methods=['POST', ])
def shownewpatientlistafterdelete():
    if request.method == 'POST':
        try:
            deleteidnumber = request.form['deleteidnumber']

            connection = psycopg2.connect(
                user="postgres", password="password", host="192.168.1.43", port="5432", database="hospitalmanagement")

            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)

            sqldelete = "DELETE FROM patients WHERE patientid = %s"
            point_to_delete = (deleteidnumber,)
            cursor.execute(sqldelete, point_to_delete)
            connection.commit()
            msg = "Patient successfully deleted"

        except (Exception, psycopg2.Error) as error:
            msg = ("Failed to delete record into patients table", error)

        finally:
            return render_template("shownewpatientlistafterdelete.html", msg=msg)
            connection.close()


@ app.route('/loggedin')
def loggedincloneback():
    return render_template("loggedin.html")


def getpatient(search):
    with psycopg2.connect(user="postgres",
                          password="password",
                          host="192.168.1.43",
                          port="5432",
                          database="hospitalmanagement") as connection:
        cursor = connection.cursor()
        # like problem in here (sql)
        searchpat = "SELECT * FROM patients WHERE patientid = %s OR pdateofbirth = %s"
        whichuser = [search, search]
        cursor.execute(searchpat, whichuser)
    results = cursor.fetchall()
    connection.close()
    return results


@ app.route("/findpatient", methods=["GET", "POST"])
def findpatient():

    if request.method == "POST":
        data = dict(request.form)
        users = getpatient(data["search"])
    else:
        users = []

    return render_template("findpatient.html", usr=users)


@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        connection = psycopg2.connect(user="postgres", password="password",
                                      host="192.168.1.43", port="5432", database="hospitalmanagement")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            UPDATE patients
            SET patientname = %s,
                patientsurname = %s,
                pplaceofbirth = %s
                pdateofbirth = %s
                pgender = %s
                pdateofjoin = %s
                patientnumber = %s
                patientemail = %s
                patientadress = %s
            WHERE patientid = %s
        """, (fname, lname, email, id))
        print('Student Updated Successfully')
        connection.commit()


# if __name__ == "__main__":
#    app.run(debug=True, port=8080, #use_reloader=False)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
