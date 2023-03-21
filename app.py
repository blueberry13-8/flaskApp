from flask import Flask, render_template, request, url_for, flash, redirect
import psycopg2
from werkzeug.exceptions import abort

app = Flask(__name__)


@app.route('/')
def index():
    con = get_db_con()
    cur = con.cursor()
    cur.execute("select * from posts")
    posts = cur.fetchall()
    con.close()
    print(posts)
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post_db = get_post(post_id)
    return render_template('post.html', post=post_db)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            con = get_db_con()
            cur = con.cursor()
            cur.execute(f"INSERT INTO posts (title, content) VALUES ('{title}', '{content}')")
            con.commit()
            con.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post_db = get_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            con = get_db_con()
            cur = con.cursor()
            cur.execute(f"UPDATE posts SET title='{title}', content='{content}' WHERE id={post_id}")
            con.commit()
            con.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post_db)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    con = get_db_con()
    cur = con.cursor()
    cur.execute(f"DELETE FROM posts WHERE id={id}")
    con.commit()
    flash('"{}" was successfully deleted!'.format(post[2]))
    return redirect(url_for('index'))


def get_post(post_id):
    con = get_db_con()
    cur = con.cursor()
    cur.execute(f"select * from posts where id={post_id}")
    post_db = cur.fetchall()
    print(post_db)
    con.close()
    if len(post_db) != 1:
        abort(404)
    return post_db[0]


def get_db_con():
    con = psycopg2.connect(dbname='flask', user='postgres',
                           password=open('password.txt').read(), host="127.0.0.1", port="5432")
    return con


if __name__ == '__main__':
    app.run()
