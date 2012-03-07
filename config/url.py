#! /bin/python
# coding:utf-8

path='controller'

urls=(
        '/',                            path+'.blog.index',
        '/article/(\d+)',               path+'.blog.article',
        '/article/edit/(\d+)',          path+'.blog.article_edit',
        '/article/edit/post/(\d+)',     path+'.blog.article_edit_post',
        '/article/add',                 path+'.blog.article_add',
        '/article/post',                path+'.blog.article_post',
        '/article/del/(\d+)',           path+'.blog.article_del',
        '/comment/add/(\d+)',           path+'.blog.comment_add',
        '/comment/del/(\d+)/(\d+)',     path+'.blog.comment_del',
        '/admin',                       path+'.blog.admin',
        '/login',                       path+'.blog.login',
        '/addusr',                      path+'.blog.addusr',
        '/logout',                      path+'.blog.logout',
        '/about',                       path+'.blog.about',
        '/about/post',                  path+'.blog.about_post',
        '/about/msg',                   path+'.blog.about_msg',
        '/about/del/(\d+)',             path+'.blog.about_del'
        
        )
