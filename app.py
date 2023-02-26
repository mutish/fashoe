import sqlite3

from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b059015be2eb355056a4945bbe691c36ef47fa82c15eadc6'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_stock(stock_id):
    conn = get_db_connection()
    stock = conn.execute('SELECT * FROM stocks WHERE id = ?',(stock_id,)).fetchone()
    conn.close()

    if stock is None:
        abort(404)
        return stock

@app.route('/')
def index():
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM stocks').fetchall()
    conn.close()
    return render_template('index.html', stocks=stocks)

@app.route('/add/', methods=('GET', 'STOCK'))
def add():
    if request.method == 'STOCK':
        title = request.form['title']
        price = request.form['price']

        if not title:
            flash("Title is required!")
        elif not price:
            flash("Please input price!")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO stocks (title,price) VALUES (?, ?)", (title, price))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/<int:id>/edit', methods=('GET','STOCKS'))
def edit(id):
    stock = get_stock(id)
    if request.method == 'STOCK':
        title = request.form['title']
        price = request.form['price']

        if not title:
            flash('Title is required!')
        elif not price:
            flash('price is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE stocks SET title = ?, price = ? '
                         'WHERE id = ?',
                         (title, price, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', stock=stock)


@app.route('/<int:id>/delete', methods=('GET', 'STOCK'))
def delete(id):
    stock = get_stock(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM stocks Where id = ?', (id,))
    conn.commit()
    conn.close()
    if stock is not None:
        flash('"{}" was successfully deleted!'.format(stock['title']))
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()

