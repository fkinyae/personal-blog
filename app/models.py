from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quotes:
    def __init__(self,author,id,quote):
        self.author=author
        self.id=id
        self.quote=quote   

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blog = db.relationship('Blog', backref = 'user', lazy="dynamic")
    comments = db.relationship('Comments',backref = 'user',lazy = "dynamic")



    
    pass_secure = db.Column(db.String(255))
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
            
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)    
    
    def __repr__(self):
        return f'User {self.username}'
    
class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(255))
    users = db.relationship('User', backref = 'role', lazy="dynamic")
    
    def __repr__(self):
        return f'User {self.name}'   
    
class Blog(db.Model):
    
    __tablename__ = 'blog'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    brief = db.Column(db.String())
    description = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()    
    
    @classmethod    
    def get_blog(cls,id):
        blogs = Blog.query.filter_by(id=id).all()
        
        return blogs  
    
class Comments(db.Model):
    
    __tablename__='comments'
    
    id = db.Column(db.Integer, primary_key=True)
    comment=db.Column(db.String)
    blog_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))    
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
     
    @classmethod   
    def get_comments(cls,id):
        comments=Comments.query.filter_by(blog_id=id).all()
        return comments   
    

    


       


    
    

      

    