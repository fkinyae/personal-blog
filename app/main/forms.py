from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import Required,Email,EqualTo
from ..models import User,Role,Blog
from wtforms import ValidationError

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
    
    
class BlogForm(FlaskForm):
    title = StringField('Blog title',validators=[Required()])
    brief = TextAreaField('Story Intro')  
    description = TextAreaField('Full Story')
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):

 comment = TextAreaField('Add Your Comment')

 submit = SubmitField('Submit')    
        
    

        