#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi

from google.appengine.api import users

from models import Email, User

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class CreateAccountHandler(BaseHandler):
    def get(self):
        return self.render_template("create-account.html")

class LoginHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class HomeHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class ReceivedHandler(BaseHandler):
    def get(self):
        return self.render_template("received.html")

class SentHandler(BaseHandler):
    def get(self):
        return self.render_template("sent.html")

class WeatherHandler(BaseHandler):
    def get(self):
        return self.render_template("weather.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', LoginHandler),
    webapp2.Route('/home', HomeHandler),
    webapp2.Route('/create-account', CreateAccountHandler),
    webapp2.Route('/received', ReceivedHandler),
    webapp2.Route('/sent', SentHandler),
    webapp2.Route('/weather', WeatherHandler),
], debug=True)
