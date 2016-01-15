from app import App
from flask import render_template, request, flash, session, url_for, redirect
from forms import SigninForm
from models import db, User
import datetime as dt
import time
import threading


class Date(object):
    end_time = dt.datetime(2016, 1, 17, 0, 58, 0, 0)

    def __init__(self):
        pass
track = Date()


def end():
    global track
    return dt.datetime.now() > track.end_time


@App.route('/')
def home():
    return render_template('home.html', title="home", msg=None, en=False)


@App.route('/about')
def about():
    return render_template('about.html', title="about")


@App.route('/contact', methods=['GET', 'POST'])
def contact():
    pass


@App.route('/next')
@App.route('/next/<subj>')
def next(subj=None):
    import json
    global track
    track = Date()
    if not end():
        if subj == "Physics":
            start = 0
            last = 30
        elif subj == "Chemistry":
            start = 30
            last = 60
        else:
            start = 60
            last = 90
        return render_template('next.html', title="next",
                               question=range(1, 91), options=['A', 'B', 'C', 'D'], data=subj if subj else None, start=start, last=last)
    else:
        return render_template('home.html', title="Contest ended", msg="Contest ended", en=True)


@App.route('/signin', methods=['GET', 'POST'])
def signin():
    if end():
        return render_template('home.html', title="Contest ended", msg="Contest ended", en=True)

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
