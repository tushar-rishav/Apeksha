from app import App
from flask import render_template, request, flash, session, url_for, redirect
from forms import SigninForm
from models import db, User


@App.route('/')
def home():
    return render_template('home.html', title="home")


@App.route('/about')
def about():
    return render_template('about.html', title="about")


@App.route('/contact', methods=['GET', 'POST'])
def contact():
    pass


@App.route('/next')
def next():
    import json
    return render_template('next.html', title="next", data = None)

@App.route('/next/<subj>')
def next_subj(subj):
    import json
    with open('app/static/question/data.json') as data_file:  
        data = json.load(data_file)
    return render_template('next.html', title="next", data = data[subj])


@App.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if 'email' in session:
        return redirect(url_for('next'))

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form, title="signin")
        else:
            session['email'] = form.Email.data
            return redirect(url_for('next'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form, title="signin")


@App.route('/signout')
def signout():

    if 'email' not in session:
        return redirect(url_for('signin'))

    session.pop('email', None)
    return redirect(url_for('home'))
