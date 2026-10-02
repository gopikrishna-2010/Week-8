from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField("Add Comment")
