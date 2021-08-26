from flask import render_template,request,url_for,abort,redirect,flash
from . import main
from flask_login import login_required, current_user
from ..models import  User,Role,Blog,Comments
from .forms import UpdateProfile,BlogForm,CommentForm
from .. import db,photos
import markdown2
from ..request import get_quotes, repeat_get_quotes


@main.route('/', methods = ['GET','POST'])
def index():
    
    blogs = Blog.query.all()
    quote = get_quotes
    quotes = repeat_get_quotes(1, get_quotes)
        
    return render_template('blog.html',blogs=blogs,quotes=quotes)
        
@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        brief = form.brief.data
        description = form.description.data
        
        new_blog = Blog(title=title,brief=brief,description=description,user=current_user)
        
        new_blog.save_blog()  
        return redirect(url_for('main.index'))
    
    return render_template('new_blog.html',blog_form=form)   

@main.route('/blog/single/<int:id>', methods = ['GET','POST'])
@login_required
def single_blog(id):
    
    id = Blog.query.filter_by().first().id
    
    blogs = Blog. get_blog(id)
        
    return render_template('single_blog.html',blogs=blogs,id=id)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    
    if user is None:
        abort(404)
        
    return render_template("profile/profile.html", user=user)    

@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
        
    form = UpdateProfile()
    
    if form.validate_on_submit():
        user.bio = form.bio.data
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile', uname=user.username))
    
    return render_template('profile/update.html',form=form)    

@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    

@main.route('/blog/comment/new/<int:id>', methods=['GET','POST'])
@login_required
def post_comment(id):
    form = CommentForm()
    blog = Blog.query.filter_by(id=id).first().id
    if form.validate_on_submit():
        comment=form.comment.data
        blog_id = Blog.query.filter_by(id=id).first().id

        
        new_comment=Comments(comment=comment,blog_id=blog_id,user=current_user)
        db.session.add(new_comment)
        db.session.commit()
        
        return redirect(url_for('main.index'))
        
    title = 'New Comment'    
    return render_template('all_comments.html',title=title, comment_form=form,blog=blog)

@main.route('/comment/<int:id>')
def single_comment(id):
    comment=Comments.query.get(id)
    if comment is not None:
        abort(404)
    format_comment=markdown2.markdown(comment.comment,extras=["code-friendly", "fenced-code-blocks"])   
    return render_template('comment.html',comment = comment,format_comment=format_comment) 

@main.route('/all_comments/<int:id>', methods=['GET','POST'])
def all_comments(id):
    form = CommentForm()
    blog_id = Blog.query.filter_by(id=id).first().id
    comments=Comments.get_comments(blog_id)
    if form.validate_on_submit():
        comment=form.comment.data
        blog_id = Blog.query.filter_by(id=id).first().id

        
        new_comment=Comments(comment=comment,blog_id=blog_id,user=current_user)
        db.session.add(new_comment)
        db.session.commit()
    
    
    return render_template('all_comments.html',blog_id=blog_id,comments=comments,comment_form=form)



    
    
