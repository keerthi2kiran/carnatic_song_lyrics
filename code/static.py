import sqlite3
import os
import re
from collections import defaultdict

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name).strip('_')

def capitalize_name(name):
    return ' '.join(word.capitalize() for word in name.split())

def fetch_songs():
    con = sqlite3.connect("songlyrics.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM songs")
    songs = cur.fetchall()
    con.close()
    return songs

def generate_index(songs):
    composers = defaultdict(list)
    languages = defaultdict(list)
    songs_sorted = sorted(songs, key=lambda x: x[1])
    
    for song in songs:
        composers[song[2]].append(song)
        languages[song[5]].append(song)
    
    sorted_composers = sorted(composers.keys(), key=str.lower)
    sorted_languages = sorted(languages.keys(), key=str.lower)

    index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Songs List</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        .container { display: flex; height: 100vh; }
        .left-pane { width: 30%; overflow-y: auto; border-right: 1px solid #ddd; padding: 10px; }
        .right-pane { width: 70%; padding: 10px; overflow-y: auto; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Songs</a>
    <div class="collapse navbar-collapse">
        <ul class="navbar-nav">
            <li class="nav-item"><a class="nav-link" href="#" onclick="showList('alphabetical')">Alphabetical</a></li>
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="composerDropdown" role="button" data-toggle="dropdown">Composer</a>
                <div class="dropdown-menu" id="composer-list">
"""
    for composer in sorted_composers:
        safe_composer = sanitize_filename(composer)
        index_content += f'<a class="dropdown-item" href="#" onclick="showComposer(\'{safe_composer}\')">{capitalize_name(composer)}</a>\n'
    
    index_content += """
                </div>
            </li>
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="languageDropdown" role="button" data-toggle="dropdown">Language</a>
                <div class="dropdown-menu" id="language-list">
"""
    for language in sorted_languages:
        index_content += f'<a class="dropdown-item" href="#" onclick="showList(\'{sanitize_filename(language)}\')">{capitalize_name(language)}</a>\n'
    
    index_content += """
                </div>
            </li>
        </ul>
    </div>
</nav>

<div class="container">
    <div class="left-pane" id="song-list">
        <h2 class="text-center mb-4">Songs List</h2>
        <ol class="list-group" id="song-items">
"""
    for song in songs_sorted:
        safe_name = sanitize_filename(song[1])
        safe_composer = sanitize_filename(song[2])
        index_content += f'<li class="list-group-item song-item" data-type="alphabetical" data-composer="{safe_composer}" data-language="{sanitize_filename(song[5])}">\n'
        index_content += f'<a href="{safe_name}.html" target="lyrics-frame">{song[0]} ({song[16]})</a>\n'
        index_content += f'</li>\n'
    
    index_content += """
        </ol>
    </div>
    <div class="right-pane">
        <iframe name="lyrics-frame" src="" allowfullscreen></iframe>
    </div>
</div>

<script>
function showList(filter) {
    $('.song-item').hide();
    if (filter === 'alphabetical') {
        $('.song-item[data-type="alphabetical"]').show();
    } else {
        $('.song-item[data-language="' + filter + '"]').show();
    }
}

function showComposer(composer) {
    $('.song-item').hide();
    $('.song-item[data-composer="' + composer + '"]').show();
}

$(document).ready(function() { showList('alphabetical'); });
</script>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

</body>
</html>
"""
    
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

def main():
    os.makedirs("docs", exist_ok=True)
    songs = fetch_songs()
    generate_index(songs)
    print("Static pages generated successfully in the 'docs' folder.")

if __name__ == "__main__":
    main()
