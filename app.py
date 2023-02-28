from flask import Flask, render_template, request
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import os.path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aime_profe.db"
db = SQLAlchemy(app)


class Asistencia(db.Model):

    __tablename__ = 'asistencia'

    index = db.Column(db.Integer, primary_key = True)
    apellido = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    ci = db.Column(db.String(20))
    asistencia = db.Column(db.Integer)
    grado = db.Column(db.String(20))
    justificativo = db.Column(db.String(100))
    fecha = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    return "Hello World"

@app.route("/cargar_planilla", methods=['GET', 'POST'])
def cargar_planilla():

    if request.method == 'POST':

        file = request.file['file']
        file.save(file.filename)
        file_path = os.path.dirname(os.path.abspath(file.name))
        df = pd.read_excel(file_path +'/'+ file.filename)
        con = sqlite3.connect("instance/aime_profe.db")
        df.to_sql('asistencia',con, if_exists= 'replace')


        return "Plantilla cargada con exito"
    else:
        return render_template("carga_planilla.html")



@app.route("/<grado>/asistencia/<fecha>")
def asistencia(grado, fecha):
    

    #Traer los datos de la BD, conSQLAlchemy
    lista_asistencia = db.session.query(Asistencia).filter_by(grado=grado).filter_by(fecha=fecha).all()
   # print(asistencia[0].nombre) 
    return render_template("asistencia.html", lista_asistencia=lista_asistencia)


# ejecutar con breakpoint
if __name__ == '__main__':
    app.run(debug=True)