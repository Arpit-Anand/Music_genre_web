from crypt import methods
import os
import random
from werkzeug.utils import secure_filename
from flask import (Blueprint, Flask, flash, g,  request, jsonify, render_template, redirect)
from flaskr.db import get_db
from flaskr.auth import login_required
from genre_rec_service import Genre_Recognition_Service
from pydub import AudioSegment

ALLOWED_EXTENSIONS = {'ogg', 'flac', 'wav', 'mp3'}
bp = Blueprint('pred', __name__, url_prefix = '/pred')
CHANGE_REQ  = {'mp3'}

def allowItFam(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/classify', methods = ('GET', 'POST'))
@login_required
def classify():
    if request.method == 'POST':
        audio_file = request.files['uploadAudio']
        if audio_file.filename == '':
            flash('No files selected')
            return redirect(request.url)
        if audio_file and allowItFam(audio_file.filename):
            if audio_file.filename.rsplit('.',1)[1].lower() in CHANGE_REQ:
                sound = AudioSegment.from_mp3(audio_file)
                sound.export(audio_file, format='wav')
            realFileName = secure_filename(audio_file.filename)
            temp = str(random.randint(0,10000))
            audio_file.save(temp)
            grs = Genre_Recognition_Service()
            predicted_genre = grs.predict(temp)
            db = get_db()
            db.execute('INSERT INTO history (usid, trackName, genre) VALUES(?,?,?)', (g.user['id'], realFileName, predicted_genre))
            db.commit()
            os.remove(temp)
            predictionMessage = f"""The song is predicted to be in {predicted_genre} genre."""
            return render_template('audio/index.html', message = predictionMessage)
    return render_template('audio/index.html')

