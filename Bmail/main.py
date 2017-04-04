#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi
import json
import hmac

from google.appengine.api import urlfetch

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

    def display_message(self, message):
        params = {'message': message}
        self.render_template('message.html', params)

class CreateAccountHandler(BaseHandler):
    def get(self):
        # 1 Preveri da uporabnik z emailom ne obstaja.
        user_name = cgi.escape(self.request.get('username'))
        email = cgi.escape(self.request.get('email'))
        name = cgi.escape(self.request.get('name'))
        password = cgi.escape(self.request.get('password'))
        last_name = cgi.escape(self.request.get('lastname'))

        user_from_base = User.query(User.email == email).fetch()
        user_from_base_email = user_from_base.email()
        if user_from_base_email == email:
            message = {"message": "User with %s already exists" % email}
            return self.display_message(message=message)
        # 2 Ustvari uporabnika.
        else:
            password_hash = hmac.new(password).hexdigest()
            save_user = User(name=name, last_name=last_name, user_name=user_name, email=email, password=password_hash)
            save_user.put()
            return self.redirect("index.html")

    def post(self):
        # 1 Preveri da uporabnik z emailom ne obstaja.
        user_name = cgi.escape(self.request.get('username'))
        email = cgi.escape(self.request.get('email'))
        name = cgi.escape(self.request.get('name'))
        password = cgi.escape(self.request.get('password'))
        last_name = cgi.escape(self.request.get('lastname'))

        user_from_base = User.query(User.email == email).fetch()
        user_from_base_email = user_from_base.email()
        if user_from_base_email == email:
            message = {"message": "User with %s already exists" % email}
            return self.display_message(message=message)
        # 2 Ustvari uporabnika.
        else:
            password_hash = hmac.new(password).hexdigest()
            save_user = User(name=name, last_name=last_name, user_name=user_name, email=email, password=password_hash)
            save_user.put()
            return self.redirect("index.html")


class LoginHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        email = cgi.escape(self.request.get('email'))
        password = cgi.escape(self.request.get('password'))
        password_hash = hmac.new(password).hexdigest()
        users = User.query(User.email == email).fetch()
        if len(users) == 0:
            message = {"message": "There is no user with %s" % email}
            return self.display_message(message=message)
        else:
            user = users[0]
            if user.password != password_hash:
                message = {"message": "Wrong password"}
                return self.display_message(message=message)

        return self.redirect("/home")


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
        url = "http://api.openweathermap.org/data/2.5/weather?q=Celje,si&units=metric&APPID=0fa4f697d72b1a4616a02c99f798df9c"
        result = urlfetch.fetch(url)
        data = json.loads(result.content)
        params = {"data": data}
        return self.render_template("weather.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', LoginHandler),
    webapp2.Route('/home', HomeHandler),
    webapp2.Route('/create-account', CreateAccountHandler),
    webapp2.Route('/received', ReceivedHandler),
    webapp2.Route('/sent', SentHandler),
    webapp2.Route('/weather', WeatherHandler),
], debug=True)
