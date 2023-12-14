from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def req():

    artist = request.form.get('artist')
    song = request.form.get('song')

    print(artist, song)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()