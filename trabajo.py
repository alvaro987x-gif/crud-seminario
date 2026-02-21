from flask import Flask, render_template, request, redirect, url_for, session
from conexion import conexion

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_123'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Por favor completa todos los campos"
        cur = conexion.cursor()
        cur.execute(
            'SELECT * FROM users WHERE email = %s AND password = %s',
            (email, password)
        )
        user = cur.fetchone()
        cur.close()

        if user:
            session['user_id'] = user[0]
            session['role'] = user[5]
            return redirect(url_for('admin'))
        else:
            return "Email o contraseña incorrectos"
    return render_template('login.html')

@app.route('/add', methods=['POST'])
def add_user():
    if session.get('role') != 'admin':
        return "Acceso no autorizado"

    username = request.form['username']
    name = request.form['fullname']
    email = request.form['email']
    edad = request.form['edad']
    distrito = request.form['distrito']
    password = request.form['password']

    cur = conexion.cursor()
    cur.execute(
        "INSERT INTO users (username, fullname, email, edad, distrito, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (username, name, email, edad, distrito, password, 'estudiante')
    )
    conexion.commit()
    cur.close()

    return redirect(url_for('admin'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if session.get('role') != 'admin':
        return "Acceso no autorizado"

    cur = conexion.cursor()
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['fullname']
        email = request.form['email']
        edad = request.form['edad']
        distrito = request.form['distrito']
        password = request.form['password']

        if password:
            cur.execute(
                "UPDATE users SET username=%s, fullname=%s, email=%s, edad=%s, distrito=%s, password=%s WHERE id=%s",
                (username, name, email, edad, distrito, password, id)
    )
        else:
            cur.execute(
                "UPDATE users SET username=%s, fullname=%s, email=%s, edad=%s, distrito=%s WHERE id=%s",
                (username, name, email, edad, distrito, id)
            )

        conexion.commit()
        cur.close()
        return redirect(url_for('admin'))

    cur.execute('SELECT * FROM users WHERE id=%s', (id,))
    data = cur.fetchone()
    cur.close()
    return render_template('edit.html', user=data)

@app.route('/delete/<int:id>')
def delete_user(id):
    if session.get('role') != 'admin':
        return "Acceso no autorizado"

    cur = conexion.cursor()
    cur.execute('DELETE FROM users WHERE id = %s', (id,))
    conexion.commit()
    cur.close()

    return redirect(url_for('admin'))

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = conexion.cursor()
    cur.execute("SELECT id, username, fullname, email, edad, distrito, password FROM users WHERE role = 'estudiante'")
    estudiantes = cur.fetchall()
    cur.close()

    return render_template(
        'admin.html',
        users=estudiantes,
        role=session['role']
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)