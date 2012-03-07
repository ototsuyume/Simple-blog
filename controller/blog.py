#! /bin/python
# coding:utf-8

import web
import sys
import md5
import random
from config.setting import db
from config.setting import render
from config.url import urls


reload(sys)
sys.setdefaultencoding('utf-8')
artt   = 'article'
commt  = 'comment'
usert  = 'user'
msg    = 'msg'

salt   = '&A102ad@#)'

app = web.application(urls,globals())

session=web.session.Session(app,web.session.DiskStore('userinfo'),initializer={"id":0,"seed":0,"hash":""})

def error404():
    return web.notfound(render.error())

def isadmin():
    if session.id == 0:
        return False
    data = db.select(usert,where="id ="+str(session.id))
    if len(data)==0:
        return False
    data = data[0]
    if md5.new((data.user+data.password+str(session.seed))).hexdigest() == session.hash:
        return True
    else:
        return False

class about_msg:
    def GET(self):
        try:
            comment = db.select(msg,limit="0,100",order="date DESC")
            return render.msg(isadmin(),comment)
        except:
            return render.error()

class about_del:
    def GET(self,cid):
        if isadmin():
            try:
                db.delete(msg,where="id ="+cid)
                raise web.seeother('/about')
            except:
                return render.error()
        else:
            return render.error()

class about_post:
    def POST(self):
        try:
            con = web.input()
            if isadmin():
                id=session.id
                user=db.select(usert,where=("id="+str(id)))[0].user
                hp='/'
                mail="none"
            else:
                mail=con.get('email','none')
                user=con.get('author','none')
                hp  =con.get('hp','')
                if hp.find("http://")!=0:
                    hp = "http://"+hp
                id=0
            data =con.get('comment','none')
            db.insert(msg,author=user,email=mail,content=web.websafe(data),id=0,homepage=hp,date=web.SQLLiteral("NOW()"),usrid=id)
            raise web.seeother('/about')
        except:
            return render.error()

class about:
    def GET(self):
        try:
            comment = db.select(msg,limit="0,10",order="date DESC")
            count = int(db.query("select count(*) from "+msg)[0]["count(*)"])
            return render.about(isadmin(),comment,count>10)
        except:
            return render.error()



class article_edit_post:
    def POST(self,aid):
        if not isadmin():
            return render.error()
        try:
            data =web.input()
            text = data.content
            atitle = data.title
            if not len(db.select(script))==0:
                db.delete(script)
            db.update(artt,where="id="+aid,title=atitle,content=text)
            raise web.seeother('/')
        except:
            return render.error()

class article_edit:
    def GET(self,aid):
        if isadmin():
            try:
                data=db.select(artt,where="id="+aid)
                return render.edit(True,int(aid),data[0])
            except:
                return render.error()
        else:
            return render.error()

class article_post:
    def POST(self):
        if not isadmin():
            return render.error()
        try:
            data =web.input()
            text = data.content
            atitle = data.title
        
            db.insert(artt,id=0,date=web.SQLLiteral("NOW()"),usrid=session.id,comment=0,title=atitle,content=text)
            raise web.seeother('/')
        except:
            return render.error()

class article_add:
    def GET(self):
        if  isadmin():
            return render.edit(True,0,0)
        else:
            return render.error()

class article_del:
    def GET(self,aid):
        if not isadmin():
            return render().error()
        db.delete(artt,where="id="+aid)
        db.delete(commt,where="articleid="+aid)
        raise web.seeother('/')


class logout:
    def GET(self):
        session.id=0
        session.hash=''
        session.seed=0
        raise web.seeother('/')

class login:
    def POST(self):
        postdata = web.input()
        usrid    = postdata.get("usrname","")
        pw       = postdata.get("password","")
        
        if pw=='' or usrid=='':
            return render.error()
        data = db.select(usert,where=('user="'+usrid+'"'))
        if(len(data)==0):
            return render.error()
        pw+= salt
        pw = md5.new(pw).hexdigest()
        if pw!=data[0].password:
            return render.error()
        seed = random.randint(0,100000)
        session.hash = md5.new((usrid+pw+str(seed))).hexdigest()
        session.id   = 1
        session.seed = seed
        raise web.seeother('/')



class admin:
    def GET(self):
        count = int(db.query("select count(*) from "+usert)[0]["count(*)"])
        return render.login(count,isadmin());


class addusr:
    def POST(self):
        #you can add user only on the first time
        if int(db.query("select count(*) from "+usert)[0]["count(*)"])!=0:
            return render.error()
        postdata = web.input()
        usrid    = postdata.get("usrname","")
        pw       = postdata.get("password","")
        pw+=salt
        pwmd5 = md5.new(pw).hexdigest()
        db.insert(usert,id=1,user=usrid,password=pwmd5);
        seed = random.randint(0,100000)
        session.hash = md5.new((usrid+pwmd5+str(seed))).hexdigest()
        session.id   = 1
        session.seed = seed
        raise web.seeother('/')
        

class comment_del:
    def GET(self,aid,cid):
        if isadmin():
            try:
                db.delete(commt,where="id ="+cid)
                count=int(db.select(artt,what="comment",where="id="+aid)[0]["comment"])-1
                db.update(artt,where="id="+aid,comment=count)
                raise web.seeother('/article/'+aid)
            except:
                return render.error()
        else:
            return render.error()

class comment_add:
    def POST(self,aid):
        try:
            articleid = int(aid)
            con = web.input()
            if isadmin():
                id=session.id
                user=db.select(usert,where=("id="+str(id)))[0].user
                mail="none"
                hp='/'
            else:
                mail=con.get('email','none')
                user=con.get('author','none')
                hp  =con.get('hp','')
                if hp.find("http://")!=0:
                    hp = "http://"+hp
                id=0
            data =con.get('comment','none')
            db.insert(commt,author=user,email=mail,content=web.websafe(data),id=0,articleid=articleid,homepage=hp,date=web.SQLLiteral("NOW()"),usrid=id)
            count=int(db.select(artt,what="comment",where=("id = "+aid))[0]["comment"])+1
            db.update(artt,where=("id = "+aid),comment=count)
            raise web.seeother('/article/'+aid)
        except:
            return render.error()
        

class article:
    def GET(self,id):
        try:
            articleid=int(id)
            
            content = db.select(artt,where="id = %d"%articleid)
            if len(content)==0:
                web.notfound()
            comment = db.select(commt,where="articleid =%d"%articleid,order="date")
            return render.article(content[0],comment,len(comment),isadmin())
        except:
            return render.error()

class index:
    def GET(self):
        try:
            page = int(web.input(p='1').p)-1
            query = db.select(artt,limit="%d,5"%(page*5),order="date DESC")
            
            if len(query)==0 and page!=0:
                return render.error()
            count = int(db.query("select count(*) from "+artt)[0]["count(*)"])
            ne=pre=0
            maxpage = count/5
            if maxpage%5 !=0:
                maxpage+=1
            if page>0:
                pre = page
            if page+1<maxpage:
                ne = page+2
            return render.index(query,pre,ne,isadmin())
        except:
            return render.error()


app.notfound=error404
