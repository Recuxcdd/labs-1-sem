from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(PROJECT_DIR, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        town = request.form.get('town', '').strip()
        visit_date = request.form.get('visit_date', '').strip()

        if town and visit_date:
            new_entry = Entry(town=town, visit_date=visit_date)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('index'))

    entries = Entry.query.all()
    return render_template('page.html', entries=entries)


@app.route('/clear', methods=['POST'])
def clear_db():
    db.session.query(Entry).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, render_template, request

# # PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     user_text = None
#     if request.method == 'POST':
#         town = request.form.get('town_field')
#         visit_date = request.form.get('visit_date_field')
#         if len(town) > 0 and len(visit_date) > 0:
#             print(town, visit_date)
#     return render_template('page.html', result=user_text)


# # @app.route('/submit', methods=['POST'])
# # def submit():
# #     user_text = request.form.get('text_field')
# #     print(user_text)
# #     return f"Вы ввели: {user_text}"


# if __name__ == '__main__':
#     app.run(debug=True)
