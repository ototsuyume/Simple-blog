#! /bin/python
# coding:utf-8

import web

web.config.debug = False;


db = web.database(dbn='mysql',db='blog',user='root',pw='123456')

render = web.template.render('template/',base="layout")

side  = web.template.render('template/')

web.template.Template.globals['render']=side
