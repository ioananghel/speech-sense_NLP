# blueprint of application -> has views and routes
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Articles
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/admin', methods=['Get', 'POST'])
@login_required
def admin():
    # ---------------------------------------- for posting (updating the db using site) ------------------------
    if(current_user.email != "admin@cti.ro"):    
        articles = Articles.query.all()
        return render_template("home.html", user=current_user, articles=articles) 

    else:
        if request.method == 'POST': 
            article_content = request.form.get('article_content')#Gets the article from the HTML 
            article_title = request.form.get('article_title')
            if len(article_content) < 1:
                flash('Article too short!', category='error') 
            if len(article_title) < 1:
                flash('Title too short!', category='error') 
            else:
                new_article = Articles(title=article_title, content=article_content, sentiment="not sure")  #providing the schema for the article 
                db.session.add(new_article) #adding the article to the database 
                db.session.commit()
                flash('Article added!', category='success')
        
        articles = Articles.query.all()
        return render_template("admin.html", user=current_user, articles=articles)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    # from .test import test_df

    # for i in range(0, len(test_df)):
    #     article = test_df.iloc[i]
    #     new_article = Articles(title=article["content"], content=article["content"], sentiment=article["trust_prediction"], category=article["category_predictions"])  #providing the schema for the article 
    #     db.session.add(new_article) #adding the article to the database 
    #     db.session.commit()
    #  # flash('Article added!', category='success')

    articles = Articles.query.all()

    # with this check if an user is logged in
    return render_template("home.html", user=current_user, articles=articles) 


@views.route('/delete-article', methods=['POST'])
def delete_article():  
    article = json.loads(request.data)# this function expects a JSON from the INDEX.js file 
    articleId = article['articleId']
    article = Articles.query.get(articleId)
    if article:
        if current_user.email == "admin@cti.ro":
            db.session.delete(article)
            db.session.commit()
    return jsonify({})


 # -------------------------------------------hardcoded article adding ------------------------    

    #------------------------------------------------------ add article script---------------------------
    
    # new_article = Articles( title="This is a test ", 
    #                         content="This Test has proven to be testy", 
    #                         sentiment="kinda testy ngl")
    # db.session.add(new_article)
    # db.session.commit()

    #------------------------------------------------------ delete article script---------------------------
    
    # articleId = 1
    # article = Articles.query.get(articleId)
    # if article:
    #     db.session.delete(article)
    #     db.session.commit()