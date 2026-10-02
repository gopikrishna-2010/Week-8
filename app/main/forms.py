from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class SearchForm(FlaskForm):
    query = StringField("Search", validators=[Length(max=100)])
    submit = SubmitField("Search")
