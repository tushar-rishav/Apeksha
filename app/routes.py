from app import App
from flask import render_template, request, flash, session, url_for, redirect
from forms import SigninForm
import datetime as dt
from models import db, Respon
class Date(object):
    end_time = dt.datetime(2017, 10, 25, 17, 32, 0, 0)

    def __init__(self):
        pass
track = Date()

subj_questions = {
    "Physics" : [0,30],
    "Chemistry": [30,60],
    "Mathematics":[60,90]
}

def end():
    global track
    return dt.datetime.now() > track.end_time

def update_response_str(db_resp, form_resp, subject):
    db_resp = list(db_resp)
    start,end = subj_questions.get(subject,[0,0])[0], subj_questions.get(subject,[0,0])[1]
    form_resp = dict(form_resp)
    for i in xrange(start,end):
        form_resp[str(i+1)] = form_resp.get(str(i+1),[u'X'])[0]
    for i in xrange(0,30):
        # try:
        #     if form_resp[str(start+i+1)] != 'X':
        db_resp[i] = form_resp[str(start+i+1)]
        # except Exception as e:
        #     print(e)
    return ''.join(db_resp)

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
    if 'reg' in session:
        import json
        global track
        track = Date()
        #print "END ",end()
        if not end():
            response = Respon.query.filter_by(reg_id=session['reg']).first()
            if not response:
                db.session.add(Respon(session['reg'], "X"*30, "X"*30, "X"*30))
                db.session.commit()
                response = Respon.query.filter_by(reg_id=session['reg']).first()
            temp = {
                "Physics":response.Physics,
                "Chemistry":response.Chemistry,
                "Mathematics":response.Mathematics
            }
            return render_template('next.html', question=range(1, 91), options=['A', 'B', 'C', 'D'],
                                    title=subj if subj else None, start=subj_questions.get(subj,[0,0])[0],
                                    last=subj_questions.get(subj,[0,0])[1], attempts = temp.get(subj,"X"*30) if subj else "X"*30 )
        else:
            return render_template('home.html', title="Contest ended", msg="Contest ended", en=True)
    else:
        return redirect(url_for('signin'))

@App.route('/next/<subj>/save',methods=['POST'])
def save(**args):
    resp_str = ""
    if 'reg' not in session:
        return redirect(url_for('signin'))
    if request.method == 'POST':
        subj = str(request.form['subject'])
        response = Respon.query.filter_by(reg_id=session['reg']).first()
        
        if not response:
            db.session.add(Respon(session['reg'], "X"*30, "X"*30, "X"*30))
            db.session.commit()
            response = Respon.query.filter_by(reg_id=session['reg']).first()
        
        
        if subj == "Physics":
            resp_str =  str(response.Physics)
            resp_str = update_response_str(resp_str, request.form, subj)
            response.Physics = resp_str

        elif subj == "Chemistry":
            resp_str =  str(response.Chemistry)
            resp_str = update_response_str(resp_str, request.form, subj)
            response.Chemistry = resp_str

        else:
            resp_str =  str(response.Mathematics)
            resp_str = update_response_str(resp_str, request.form, subj)
            response.Mathematics = resp_str
        db.session.commit()

    return render_template('next.html', question=range(1, 91), options=['A', 'B', 'C', 'D'],
                            title=subj if subj else None, start=subj_questions.get(subj,[0,0])[0],
                            last=subj_questions.get(subj,[0,0])[1], attempts = resp_str)


    
@App.route('/signin', methods=['GET', 'POST'])
def signin():
    if end():
        return render_template('home.html', title="Contest ended", msg="Contest ended", en=True)

    form = SigninForm(request.form)

    print "FORM", form.__dict__
    print "SESSION", session.__dict__

    if 'reg' in session:
        return redirect(url_for('next'))

    if request.method == 'POST':
        if form.validate_form() == False:
            return render_template('signin.html', form=form, title="signin")
        else:
            session['reg'] = form.reg.data
            return redirect(url_for('next'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form, title="signin")


@App.route('/signout')
def signout():
    if 'reg' not in session:
        return redirect(url_for('signin'))

    session.pop('reg', None)
    return redirect(url_for('home'))
