from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# NOTE: Esta parte fue completada con ayuda de Copilot.
baseDir = os.path.abspath(os.path.dirname(__file__))

# Configuración de la aplicación Flask y SQLAlchemy
# Aquí se establece la conexión con la base de datos SQLite
# y se crea la instancia de la aplicación Flask.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'Database', 'creditos.db')
db = SQLAlchemy(app)

# Modelo/Entidad/Tabla de Créditos
# TODO: Este modelo podría haberse colocado en un archivo separado, como se hace comúnmente en frameworks como Spring.
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

# Ruta para redirigir al formulario de registro de crédito
@app.route('/redirigirRegistrarCredito')
def redirigirRegistrarCredito():
    return render_template('registrarCredito.html')

# Ruta para visualizar todos los créditos registrados
@app.route('/verCreditos')
def verCreditos():
    # Se obtiene la lista completa de créditos usando el ORM de SQLAlchemy.
    creditos = Credito.query.all()
    # Los créditos se envían a la plantilla para su visualización.
    return render_template('verCreditos.html', creditos=creditos)

# Ruta para registrar un nuevo crédito
@app.route('/registrarCredito', methods=['POST'])
def registrarCredito():
    # Paso 1: Recibir los datos del formulario e instanciar el modelo Credito.
    # Cada campo debe coincidir con los atributos definidos en el modelo.
    nuevoCredito = Credito(
        cliente=request.form['cliente'],
        monto=float(request.form['monto']),
        tasaInteres=float(request.form['tasaInteres']),
        plazo=int(request.form['plazo']),
        fechaOtorgamiento=request.form['fechaOtorgamiento']
    )

    # Paso 2: Agregar el nuevo crédito a la sesión de base de datos.
    db.session.add(nuevoCredito)

    # Paso 3: Confirmar los cambios en la base de datos.
    db.session.commit()

    # Paso 4: Permanecer en la vista actual de registro.
    return render_template('registrarCredito.html')

# Ruta para eliminar un crédito
@app.route('/eliminarCredito/<int:id>')
def eliminarCredito(id):
    # Se busca el crédito por ID y se elimina directamente.
    Credito.query.filter_by(id=id).delete()

    # Confirmar los cambios tras la eliminación.
    db.session.commit()
    return redirect('/verCreditos')

# Ruta para editar un crédito existente
@app.route("/editarCredito/<int:id>", methods=["GET", "POST"])
def editarCredito(id):
    # Se obtiene el crédito mediante su ID o se lanza un error 404 si no existe.
    credito = Credito.query.get_or_404(id)

    # NOTE: Esta función es más compleja, fue desarrollada después de las rutas básicas.
    # TODO: Considerar subir cambios al repositorio ahora que esta funcionalidad ya está terminada.

    if request.method == "POST":
        # Actualizar los datos del crédito con la información del formulario.
        credito.cliente = request.form["cliente"]
        credito.monto = float(request.form["monto"])
        credito.tasaInteres = float(request.form["tasaInteres"])
        credito.plazo = int(request.form["plazo"])
        credito.fechaOtorgamiento = request.form["fechaOtorgamiento"]

        # Guardar los cambios en la base de datos.
        db.session.commit()
        return redirect(url_for("verCreditos"))
    
    # NOTE: Llegado a este punto, todo funciona correctamente y los cambios pueden subirse al repositorio.
    return render_template("actualizarCredito.html", credito=credito)

# Ruta para enviar los datos necesarios para generar la gráfica
@app.route('/datosGrafica')
def datosGrafica():
    # Se obtiene toda la información de los créditos registrados.
    creditos = Credito.query.all()

    # Se extraen los datos específicos que se utilizarán en la gráfica.
    cliente = [credito.cliente for credito in creditos]
    monto = [credito.monto for credito in creditos]

    return render_template("grafica.html", cliente=cliente, monto=monto)

if __name__ == '__main__':
    app.run(debug=True)
