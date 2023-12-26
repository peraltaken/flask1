from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "mydb"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


def data_fetch(query):
    cur = mysql.connection.cursor()
    query = """
        select * from customers"""

    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def home_page():
    return render_template('home.html')


@app.route("/customers", methods=["GET"])
def show_clients():
    customers_data = data_fetch("""select * from customers""")
    return render_template('customer.html', customers=customers_data)

@app.route("/add")
def add_client():
    return render_template('add.html')

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        last_name = request.form["last_name"]
        first_name = request.form["first_name"]
        email = request.form["email"]
        phonenumber = request.form["phonenumber"]
        country = request.form["country"]


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customers (last_name, first_name, email, phonenumber, country) VALUES (%s, %s, %s, %s, %s)", (last_name, first_name, email, phonenumber, country))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('show_customers'))


@app.route("/edit/<int:customers_id>", methods=["GET", "POST"])
def edit_customer(idCustomers):
    cur = mysql.connection.cursor()
    
    if request.method == "POST":
        new_last_name = request.form["new_last_name"]
        new_first_name = request.form["new_first_name"]
        new_email = request.form["new_email"]
        new_phonenumber = request.form["new_phonenumber"]
        new_country = request.form["new_country"]
        
        cur.execute("""
            UPDATE clients 
            SET 
                last_name = %s, 
                first_name = %s, 
                email = %s, 
                phonenumber = %s, 
                country = %s 
            WHERE 
                idCustomers = %s
        """, (
            new_last_name,
            new_first_name,
            new_email,
            new_phonenumber,
            new_country,
            idCustomers
        ))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('show_customers'))
    
    # Fetch existing client details to pre-fill the edit form
    cur.execute("SELECT * FROM customers WHERE idCustomers = %s", (idCustomers,))
    customer_data = cur.fetchone()
    cur.close()
    
    return render_template('edit.html', customer=customer_data)

@app.route("/delete/<int:idCustomers>")
def delete_customers(idCustomers):
    cur = mysql.connection.cursor()
    
    cur.execute("DELETE FROM customers WHERE idCustomers = %s", (idCustomers,))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('show_customers'))

@app.route("/customers/<int:idCustomers>")
def show_single_customer(idCustomers):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM customers WHERE idCustomers = %s", (idCustomers,))
    customers_data = cur.fetchone()
    cur.close()

    return render_template('single_customer.html', customer=customers_data)

@app.route("/customers/<string:customers_last_name>")
def show_single_client_by_name(customers_last_name):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM customers WHERE last_name = %s", (customers_last_name,))
    customers_data = cur.fetchone()
    cur.close()

    return render_template('single_customers.html', customer=customers_data)

if __name__ == "__main__":
    app.run(debug=True)