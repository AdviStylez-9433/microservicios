from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/microservicios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'
    
    id = db.Column(db.Integer, primary_key=True)
    rut_estudiante = db.Column(db.String(12))  # Elimina la relación ForeignKey temporalmente
    semestre = db.Column(db.String(10))
    asignatura = db.Column(db.String(50))
    evaluacion = db.Column(db.Float)

@app.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    data = request.json
    nueva_evaluacion = Evaluacion(
        rut_estudiante=data['rut_estudiante'],
        semestre=data['semestre'],
        asignatura=data['asignatura'],
        evaluacion=data['evaluacion']
    )
    db.session.add(nueva_evaluacion)
    db.session.commit()
    return jsonify({"mensaje": "Evaluación creada"}), 201

@app.route('/evaluaciones', methods=['GET'])
def obtener_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    return jsonify([{
        "id": e.id,
        "rut_estudiante": e.rut_estudiante,
        "semestre": e.semestre,
        "asignatura": e.asignatura,
        "evaluacion": e.evaluacion
    } for e in evaluaciones])

@app.route('/evaluaciones/<id>', methods=['GET'])
def obtener_evaluacion(id):
    evaluacion = Evaluacion.query.get(id)
    if evaluacion:
        return jsonify({
            "id": evaluacion.id,
            "rut_estudiante": evaluacion.rut_estudiante,
            "semestre": evaluacion.semestre,
            "asignatura": evaluacion.asignatura,
            "evaluacion": evaluacion.evaluacion
        })
    return jsonify({"mensaje": "Evaluación no encontrada"}), 404

def initialize_database():
    max_retries = 10  # Aumentamos los reintentos
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
    
    print("Advertencia: No se pudo crear tablas (puede que ya existan)")
    # Continuamos aunque falle, pues las tablas podrían estar creadas por el otro servicio

if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5001)