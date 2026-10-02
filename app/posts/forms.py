from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=200)])
    category = StringField("Category", validators=[DataRequired(), Length(max=80)])
    tags = StringField("Tags", validators=[Length(max=250)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10)])
    image = FileField("Image", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only.")])
    published = BooleanField("Published", default=True)
    submit = SubmitField("Save Post")
