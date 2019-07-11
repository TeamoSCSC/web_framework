from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    """
    weibo 首页的路由函数
    """
    if 'user_id' in request.query:
        user_id = int(request.query['user_id'])
        u = User.one(id=user_id)
    else:
        u = current_user(request)
    weibos = Weibo.all(user_id=u.id)
    return html_response('weibo_index.html', weibos=weibos, user=u)


def add(request):
    u = current_user(request)
    form = request.form()
    Weibo.add(form, u.id)
    log('weibo add', u, form)
    return redirect('/weibo/index')


def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        c.delete(c.id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query['id'])
    w = Weibo.one(id=weibo_id)
    return html_response('weibo_edit.html', weibo=w)


def update(request):
    form = request.form()
    weibo_id = int(form['id'])
    Weibo.update(weibo_id, content=form['content'])
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    form = request.form()
    weibo_id = int(form['weibo_id'])

    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo_id
    Comment.new(c.__dict__)

    log('comment add', c, u, form)
    return redirect('/weibo/index')


def comment_delete(request):
    user_id = request.query['user_id']
    comment_id = int(request.query['c_id'])
    Comment.delete(comment_id)
    return redirect('/weibo/index?user_id={}'.format(user_id))


def comment_edit(request):
    comment_id = int(request.query['c_id'])
    c = Comment.one(id=comment_id)
    return html_response('comment_edit.html', comment=c)


def comment_update(request):
    form = request.form()
    comment_id = int(form['c_id'])
    c = Comment.one(id=comment_id)
    weibo_id = int(c.weibo_id)
    w = Weibo.one(id=weibo_id)
    user_id = int(w.user_id)
    Comment.update(comment_id, content=form['content'])

    return redirect('/weibo/index?user_id={}'.format(user_id))


def weibo_owner_required(route_function):
    def f(request):
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.one(id=int(weibo_id))

        if int(w.user_id) == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')
    return f


def route_dict():
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        '/weibo/index': login_required(index),
        # 评论功能
        '/comment/add': login_required(comment_add),
        '/comment/delete': login_required(comment_delete),
        '/comment/edit': login_required(comment_edit),
        '/comment/update': login_required(comment_update),
    }
    return d
