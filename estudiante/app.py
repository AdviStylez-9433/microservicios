from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/microservicios'
db = SQLAlchemy(app)

class Estudiante(db.Model):
    rut = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    curso = db.Column(db.String(20))

@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.json
    nuevo_estudiante = Estudiante(
        rut=data['rut'],
        nombre=data['nombre'],
        edad=data['edad'],
        curso=data['curso']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify({"mensaje": "Estudiante creado"}), 201

@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([{
        "rut": e.rut,
        "nombre": e.nombre,
        "edad": e.edad,
        "curso": e.curso
    } for e in estudiantes])

@app.route('/estudiantes/<rut>', methods=['GET'])
def obtener_estudiante(rut):
    estudiante = Estudiante.query.get(rut)
    if estudiante:
        return jsonify({
            "rut": estudiante.rut,
            "nombre": estudiante.nombre,
            "edad": estudiante.edad,
            "curso": estudiante.curso
        })
    return jsonify({"mensaje": "Estudiante no encontrado"}), 404

def initialize_database():
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("¡Tablas creadas exitosamente!")
            return
        except Exception as e:
            print(f"Intento {attempt + 1} de {max_retries}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    print("No se pudo conectar a la base de datos después de varios intentos")
    exit(1)

if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5000)