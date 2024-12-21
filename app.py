from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia por tu usuario de MySQL
app.config['MYSQL_PASSWORD'] = ''  # Cambia por tu contraseña
app.config['MYSQL_DB'] = 'telefono_db'

# Inicialización de MySQL
mysql = MySQL(app)

# Clave secreta para mensajes flash
app.secret_key = 'mi_clave_secreta'

# Ruta principal (mostrar todos los registros)
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM telefonos')
    registros = cur.fetchall()
    cur.close()
    return render_template('index.html', registros=registros)

# Ruta para agregar un nuevo teléfono
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO telefonos (nombre, telefono, email) VALUES (%s, %s, %s)', (nombre, telefono, email))
        mysql.connection.commit()
        cur.close()

        flash('Teléfono agregado exitosamente', 'success')
        return redirect(url_for('index'))
    
    return render_template('agregar.html')

# Ruta para editar un teléfono
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM telefonos WHERE id = %s', [id])
    telefono = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE telefonos SET nombre = %s, telefono = %s, email = %s WHERE id = %s',
                    (nombre, telefono, email, id))
        mysql.connection.commit()
        cur.close()

        flash('Teléfono actualizado exitosamente', 'success')
        return redirect(url_for('index'))

    return render_template('editar.html', telefono=telefono)

# Ruta para eliminar un teléfono
@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM telefonos WHERE id = %s', [id])
    mysql.connection.commit()
    cur.close()

    flash('Teléfono eliminado exitosamente', 'danger')
    return redirect(url_for('index'))

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
