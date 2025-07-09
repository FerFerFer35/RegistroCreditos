from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Esto me ayudo Copilot a completarlo
baseDir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'Database', 'creditos.db')
db = SQLAlchemy(app)

# Modelo/Entidad/Tabla de Creditos
# Debimos de haber creado el modelo en otro archivo como lo hacemos en Spring (si lo recuerdas lo haces).
class Credito(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    tasaInteres = db.Column(db.Float, nullable=False)
    plazo = db.Column(db.Integer, nullable=False)
    fechaOtorgamiento = db.Column(db.String(10), nullable=False)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para registrar
@app.route('/redirigirRegistrarCredito')
def redirigirRegistrarCredito():
    return render_template('registrarCredito.html')

# Ruta para ver todos los créditos
@app.route('/verCreditos')
def verCreditos():
    # Es necesario englobar la consulta a la base de datos en una variable para enviar los datos a la plantilla.
    # Con la funcion query.all() del ORM obtenemos todos los registros de la tabla.
    creditos = Credito.query.all()
    # Nota: Enviar los datos en el return para mostrar en la plantilla.
    return render_template('verCreditos.html', creditos=creditos)

# Registrar crédito
@app.route('/registrarCredito', methods=['POST'])
def registrarCredito():
    # Pasos para entender el funcionamiento:
    # 1. Recibir los datos del formulario, e instancial con el modelo Credito.
    # Cada campo del formulario debe coincidir con los atributos del modelo.
    nuevoCredito = Credito(
        cliente=request.form['cliente'],
        monto=float(request.form['monto']),
        tasaInteres=float(request.form['tasaInteres']),
        plazo=int(request.form['plazo']),
        fechaOtorgamiento=request.form['fechaOtorgamiento']
    )

    # 2. Utlizamos el ORM de SQLAlchemy (similar a Laravel y Spring) para agregar el nuevo crédito a la base de datos.
    db.session.add(nuevoCredito)
    # 3. Commit para guardar los cambios en la base de datos.
    db.session.commit()
    # 4. Redirigir a la página de ver créditos.
    return render_template('registrarCredito.html')

# Eliminar crédito
@app.route('/eliminarCredito/<int:id>')
def eliminarCredito(id):
    # Solo filtra y concatena la funcion .delete() para eliminar el registro.
    Credito.query.filter_by(id=id).delete()
    # Acuérdate de hacer commit para guardar los cambios en la base de datos.
    db.session.commit()
    return redirect('/verCreditos')

# Editar crédito
@app.route("/editarCredito/<int:id>", methods=["GET", "POST"])
def editarCredito(id):
    # Función de editar, un poco más compleja, la creamos después
    # Sera necesario subir cambios al repositorio?: -> Mejor lo subimos ya que hayamos completado el proyecto.
    # Continuamos aqui después ⬇️
    credito = Credito.query.get_or_404(id)

    # Utiliza get_or_404 por si no esxiste ⬆️
    # ⬆️ debe de axistir siempre por que lo concatenamos con un boton
    if request.method == "POST":
        credito.cliente = request.form["cliente"]
        credito.monto = float(request.form["monto"])
        credito.tasaInteres = float(request.form["tasaInteres"])
        credito.plazo = int(request.form["plazo"])
        credito.fechaOtorgamiento = request.form["fechaOtorgamiento"]

        db.session.commit()
        return redirect(url_for("verCreditos"))
    
    # Ahora si sube los cambios al repositorio ya que todo funciona correctamente.

    return render_template("actualizarCredito.html", credito=credito)


@app.route('/datosGrafica')
def datosGrafica():
    # Consulta para obtener los datos de los créditos
    creditos = Credito.query.all()

    # Datos para la gráfica
    cliente = [credito.cliente for credito in creditos]
    monto = [credito.monto for credito in creditos]

    return render_template(
        "grafica.html", cliente=cliente, monto=monto)


if __name__ == '__main__':
    app.run(debug=True)
