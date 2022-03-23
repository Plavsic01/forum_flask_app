from flask import Flask, redirect,render_template, request, url_for
import pymysql
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL(app,cursorclass=pymysql.cursors.DictCursor)
        

app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_PORT"] = 3306
app.config["MYSQL_DATABASE_USER"] = "" # ENTER YOUR USERNAME
app.config["MYSQL_DATABASE_PASSWORD"] = "" # ENTER YOUR PASSWORD
app.config["MYSQL_DATABASE_DB"] = "" # ENTER YOUR SCHEMA NAME


@app.route("/")
def home():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id_objava,naslov,opis,useri_user_name FROM objave")
    objave = cursor.fetchall()
    return render_template("index.html",objave=objave)



@app.route("/dodaj-objavu",methods=["GET","POST"])
def dodaj_objavu():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_name FROM useri")
    autori = cursor.fetchall()

    if request.method == "POST":    
        objava = dict(request.form)
        print(objava)
        cursor.execute("INSERT INTO objave(naslov,opis,useri_user_name) VALUES (%s,%s,%s)" \
        ,(objava['naslov'],objava['opis'],objava['user_name']))
        db.commit()
        return redirect(url_for('home'))
    
    return render_template("nova_objava.html",autori=autori)


@app.route("/dodaj-autora",methods=["GET","POST"])
def dodaj_autora():
    if request.method == "POST":
        db = mysql.get_db()
        cursor = db.cursor()
        autor = dict(request.form)["user_name"]
        cursor.execute("INSERT INTO useri(user_name) VALUES (%s)",(autor))
        db.commit()
        return redirect(url_for('home'))

    return render_template("kreiraj_autora.html")


@app.route("/izmeni/<int:id_objava>",methods=["GET","POST"])
def izmeni(id_objava):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id_objava,naslov,opis,useri_user_name FROM objave WHERE id_objava=%s",(id_objava))
    objava = cursor.fetchone()
    if request.method == "POST":
        nova_objava = dict(request.form)
        print(nova_objava)
        cursor.execute("UPDATE objave SET naslov=%s, opis=%s WHERE id_objava=%s"\
            ,(nova_objava['naslov'],nova_objava['opis'],id_objava))
        db.commit()
        return redirect(url_for('home'))
    return render_template("izmeni_objavu.html",objava=objava)


@app.route("/obrisi/<int:id_objava>")
def obrisi(id_objava):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM objave WHERE id_objava=%s",(id_objava))
    db.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()