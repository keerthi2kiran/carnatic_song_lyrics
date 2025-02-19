from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def query_db(query, args=(), one=False):
    con = sqlite3.connect("songlyrics.db")
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    con.close()
    return (rv[0] if rv else None) if one else rv

def update_lyrics_in_db(name, lyrics):
    con = sqlite3.connect("songlyrics.db")
    cur = con.cursor()
    cur.execute('UPDATE songs SET Lyrics = ? WHERE Name = ?', (lyrics, name))
    con.commit()
    con.close()

@app.route('/')
def index():
    songs = query_db("SELECT * FROM songs")
    return render_template('index.html', songs=songs)

@app.route('/song/<name>')
def song_detail(name):
    song = query_db('SELECT * FROM songs WHERE Name = ?', [name], one=True)
    if song is None:
        return "Song not found", 404
    return render_template('song_detail.html', song=song)

@app.route('/editp/<name>', methods=['GET', 'POST'])
def edit_pallavi(name):
    if request.method == 'GET':
        # Display the form for editing lyrics
        song = query_db('SELECT * FROM songs WHERE Name = ?', [name], one=True)
        if song is None:
            return "Song not found", 404
        return render_template('edit_pallavi.html', song=song)
    elif request.method == 'POST':
        # Update the lyrics in the database
        new_lyrics = request.form['new_lyrics']
        update_lyrics_in_db(name, new_lyrics)
        return redirect(f'/song/{name}')

@app.route('/edita/<name>', methods=['GET', 'POST'])
def edit_anupallavi(name):
    if request.method == 'GET':
        # Display the form for editing lyrics
        song = query_db('SELECT * FROM songs WHERE Name = ?', [name], one=True)
        if song is None:
            return "Song not found", 404
        return render_template('edit_anupallavi.html', song=song)
    elif request.method == 'POST':
        # Update the lyrics in the database
        new_lyrics = request.form['new_lyrics']
        update_lyrics_in_db(name, new_lyrics)
        return redirect(f'/song/{name}')

@app.route('/editc/<name>', methods=['GET', 'POST'])
def edit_charanam(name):
    if request.method == 'GET':
        # Display the form for editing lyrics
        song = query_db('SELECT * FROM songs WHERE Name = ?', [name], one=True)
        if song is None:
            return "Song not found", 404
        return render_template('edit_charanam.html', song=song)
    elif request.method == 'POST':
        # Update the lyrics in the database
        new_lyrics = request.form['new_lyrics']
        update_lyrics_in_db(name, new_lyrics)
        return redirect(f'/song/{name}')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
