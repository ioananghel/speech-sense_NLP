# blueprint of application -> has views and routes
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import Articles
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    # ---------------------------------------- for posting (updating the db using site) ------------------------
    # if request.method == 'POST': 
    #     note = request.form.get('note')#Gets the note from the HTML 

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error') 
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
    #         db.session.add(new_note) #adding the note to the database 
    #         db.session.commit()
    #         flash('Note added!', category='success')

    
    # adding some filler content to test stuff out ------------------------- Delete later -------------------
    
    # new_article = Articles( title="This semester.. Can it get any worse??", 
    #                         content="This semester has proven to be an incredibly challenging one, perhaps the hardest I have ever experienced. From the overwhelming workload to the demanding course requirements, it feels like an uphill battle at every turn. The constant juggling of assignments, projects, and exams leaves little room for respite or personal time. The added pressure of adapting to online learning environments, with its technical glitches and reduced opportunities for in-person interaction, further compounds the difficulties. The absence of the usual support systems, such as classmates and professors readily available for assistance, amplifies the sense of isolation and frustration. Despite these obstacles, I am determined to persevere and give my best effort, knowing that overcoming this formidable semester will ultimately shape me into a stronger and more resilient individual.", 
    #                         sentiment="The AI thinks everything's gonnna be alright")
    # db.session.add(new_article)
    # db.session.commit()

    #------------------------------------------------------ add article script---------------------------
    
    # articleId = 1
    # article = Articles.query.get(articleId)
    # if article:
    #     db.session.delete(article)
    #     db.session.commit()

    articles = Articles.query.all()

    # with this check if an user is logged in
    return render_template("home.html", user=current_user, articles=articles) 


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
