from flask import Flask
from datetime import date
from datetime import datetime
import json
import requests
from spot import spot

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/save")
def save():
    save_artist("https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4")
    return "<p>Saved!</p>"

@app.route("/view")
def view_all():
    data = view()
    return data

@app.route("/update")
def update_artist():
    artistnu = {"id": 1, "name": "bennu"}
    up = update(artistnu)
    if up is True:
        return "<p>Updated!</p>"
    else: 
        return "<p>Update failed for some reason</p>"
    
@app.route("/delete")
def delete_artist():
    artistnu = {"id": 2}
    dr = delete(artistnu['id'])
    if dr is True:
        return "<p>Deleted artist</p>"
    else:
        return "<p>Delete failed for some reason</p>"

@app.route("/count")
def count():
    # Drake URI: 3TVXtAsR1Inumwj472S9r4
    gc = get_count("3TVXtAsR1Inumwj472S9r4")
    return str(gc)


# =============================== #

###
# Saves the specified artist to the database
# 'artist' param must be a Spotify URI
###
def save_artist(artist):
    # 0. Get URI and find Artist data (name & follower count)
    uri = str(artist).split('/')[4]
    artist_data = spot(uri)
    # 1. Open JSON file
    db = {}
    with open('artists.json') as f:
        db = json.load(f)
    # 2. Read JSON file & get artist list
    artists = db['artists']
    # 3. Check if artist exists. Return if it does
    for a in artists:
        if a['name'] == artist_data['name']:
            print('Found')
            return False
    # 4. If not, proceed to create artist object (id, count, timestamp)
    count = get_count(uri)
    date_added = datetime.now().replace(microsecond=0).strftime("%m/%d/%Y, %H:%M:%S")
    new_artist = {
        'id': len(artists)+1,
        'name': artist_data['name'],
        'count': count,
        'followers': artist_data['followers'],
        'date': date_added,
        'tags': []
    }
    # 5. Add artist obj to JSON
    artists.append(new_artist)
    db['artists'] = artists
    updated_db = json.dumps(db, indent=4)
    # 5. Write to JSON file
    with open('artists.json', 'w') as f:
        f.write(updated_db)
    return True

# Return all data for viewing
def view():
    db = {}
    with open('artists.json') as f:
        db = json.load(f)
    return db

# Update given artist 
# 'artist' should be an artist object, at least with "id" and "name"
def update(artist):
    db = {}
    with open('artists.json') as f:
        db = json.load(f)
    # Find artist in DB
    found = find_artist_by_id(db, artist['id'])
    if found:
        artist_obj = found
    else: 
        return False
    # Identify which attributes to update. For now, can only edit 'name' and 'tags':
    if "name" in artist:
        artist_obj['name'] = artist['name']
    # if "tags" in artist:
    #     artist_obj['tags'] = artist['tags']
    updated_db = json.dumps(db, indent=4)
    # Update attributes & modify DB
    with open('artists.json', 'w') as f:
        f.write(updated_db)
    return True


# Delete a single artist by id
def delete(id):
    db = {}
    with open('artists.json') as f:
        db = json.load(f)
    found = find_artist_by_id(db, id)
    if not found:
        return False
    db['artists'][:] = [d for d in db['artists'] if d.get('id') != id]
    updated_db = json.dumps(db)
    return save_db(updated_db)
    

# Return artist object if found in Db, otherwise return False
def find_artist_by_id(db, id):
    for a in db['artists']:
        if a['id'] == id:
            return a
    return False

# Pass in JSON database and write to file
def save_db(updated_db):
    with open('artists.json', 'w') as f:
        f.write(updated_db)
    return True


# ====== Auxilliary Functions ============ #

### 
# Function to retrieve count from Spotify API
# Takes in a Spotify URI
def get_count(artist_uri):
    # artist_uri = '3TVXtAsR1Inumwj472S9r4'
    # print('getting uri: ', artist_uri)
    request_url = f'http://127.0.0.1:8000/grab/{artist_uri}'
    r = requests.get(request_url)
    if r.status_code == 200:
        return int(r.text)
    else:
        return False