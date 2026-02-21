from flask import Flask, render_template, request, redirect, url_for
from conexion import conexion

app = Flask(__name__)


@app.route('/')
def index():
    cur = conexion.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    return render_template('index.html', users=data)

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = conexion.cursor()
        cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conexion.commit()
        cur.close()
        return redirect(url_for('index'))
    

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = conexion.cursor()
        cur.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
        conexion.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur = conexion.connection.cursor()
        cur.execute('SELECT * FROM users WHERE id = %s', (id,))
        data = cur.fetchone()
        cur.close()
        return render_template('edit.html', user=data)
    
@app.route('/delete/<int:id>')
def delete_user(id):    
    cur = conexion.cursor()
    cur.execute('DELETE FROM users WHERE id = %s', (id,))
    conexion.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)