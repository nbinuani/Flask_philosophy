#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, abort, url_for
from getpage import getPage

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"


@app.route('/', methods=['GET'])
def index():
    # on peut aussi utiliser url_for('static', lien de l'image wiki en logo) etc ...
    return render_template('index.html', message="Bonjour, monde !")

# Si vous définissez de nouvelles routes, faites-le ici

# 3.3
@app.route('/new-game', methods=['POST'])
def new_game():
    session['score'] = 0 # init score
    new_title = request.form['start'] # init title starting page
    session['article'] = new_title
    return redirect('/game')
    
# 3.4
@app.route('/game', methods=['GET'])
def game():
    page = session['article']
    # 3.5
    session['title'], session['content'] = getPage(page)
    if (session['title'] is None) and (session['score'] == 0):
        flash("Vous avez perdu ! Vous n'avez pas entrer de mot ... (Si vous voulez recommencer une partie en cliqueant sur le texte !)", 'perdu')
        return redirect('/')
    if (session['score'] == 0) and (session['title'] == 'Philosophie'):
        flash("Vous avez perdu ! Vous avez essayer un mot trop proche de philosophie ... (Si vous voulez recommencer une partie en cliqueant sur le texte !)", 'perdu')
        return redirect('/')
    if (session['score'] == 0) and (not session['content']):
        flash("Vous avez perdu ! Vous avez essayé une page sans contenu ... (Si vous voulez recommencer une partie en cliqueant sur le texte !)", 'perdu')
        return redirect('/')
    else:
        return render_template('game.html')


@app.route('/move', methods=['POST'])
def move():
    session['score'] = session['score'] + 1 # +=1
    new_page = request.form['destination']
    # if target == 'cheated': question 5.1 but not well keepp on other questions ...
    if new_page not in session['content']:
        flash("Vous avez triché ! Retenter votre coup en respectant les règles ... (Si vous voulez recommencer une partie en cliqueant sur le texte !)", 'perdu')
        return redirect('/')
    if new_page == 'Philosophie':
        flash("Félicitations ! Vous avez gagné avec un score de {}! \n Si vous voulez recommencer une partie \n Cliquez sur le texte !".format(session['score']), 'gagne')
        return redirect('/')
    else:
        session['article'] = new_page
        return redirect('/game')

if __name__ == '__main__':
    app.run(debug=True)

