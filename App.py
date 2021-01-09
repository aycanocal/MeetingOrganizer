from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = b'\xd76m\x8e>\xb6tK+\xac\x125IuzP'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/meeting-organizer"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String(100))
    date = db.Column(db.Date)
    startHour = db.Column(db.Time)
    finishHour = db.Column(db.Time)
    participants = db.Column(db.String(100))

    def __init__(self, topic, date, startHour, finishHour, participants):
        self.topic = topic
        self.date = date
        self.startHour = startHour
        self.finishHour = finishHour
        self.participants = participants


@app.route('/')
def Index():
    meetings = Meeting.query.all()
    return render_template("index.html", meetings=meetings)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        topic = request.form['topic']
        date = request.form['date']
        startHour = request.form['startHour']
        finishHour = request.form['finishHour']
        participants = request.form['participants']

        meeting = Meeting(topic, date, startHour, finishHour, participants)
        db.session.add(meeting)
        db.session.commit()

        return redirect(url_for('Index'))

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        meeting = Meeting.query.get(request.form.get('id'))

        meeting.topic = request.form['topic']
        meeting.date = request.form['date']
        meeting.startHour = request.form['startHour']
        meeting.finishHour = request.form['finishHour']
        meeting.participants = request.form['participants']

        db.session.add(meeting)
        db.session.commit()

        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    meeting = Meeting.query.get(id)
    db.session.delete(meeting)
    db.session.commit()

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run()