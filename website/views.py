from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
import json

from werkzeug.utils import redirect

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_in_session' not in session:
        flash('You must log-in before!', category='error')
        return redirect(url_for('auth.login'))

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    # note = json.loads(request.data)
    # noteId = note['noteId']
    # note = Note.query.get(noteId)
    #
    # if note:
    #     if note.user_id == current_user.id:
    #         db.session.delete(note)
    #         db.session.commit()

    return jsonify({})
