#!/usr/bin/env python
import os
import jinja2
import webapp2
import json
import cgi

from google.appengine.api import urlfetch

from google.appengine.api import users

from models import Email

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

        user = users.get_current_user()
        params["user"] = user

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')
            params["logout_url"] = logout_url
        else:
            logged_in = False
            login_url = users.create_login_url('/loading')
            params["login_url"] = login_url

        params["logged_in"] = logged_in

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class LoadingHandler(BaseHandler):
    def get(self):
        return self.render_template("loading.html")


class ReceivedHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            emails = Email.query(Email.receiver == email, Email.deleted == False).fetch()
            params = {"emails": emails}
            return self.render_template("received.html", params)

    def post(self):
        sender = self.request.get("sender")
        receiver = cgi.escape(self.request.get("receiver"))
        subject = cgi.escape(self.request.get("subject"))
        email = cgi.escape(self.request.get("email"))
        save_email = Email(sender=sender, receiver=receiver, subject=subject, email=email)
        save_email.put()
        return self.redirect("/received")


class EachReceivedEmailHandler(BaseHandler):
    def get(self, email_id):
        email = Email.get_by_id(int(email_id))
        params = {"email": email}
        return self.render_template("received-details.html", params)


class SentHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            emails = Email.query(Email.sender == email, Email.deleted == False).fetch()
            params = {"emails": emails}
            return self.render_template("sent.html", params)


class EachSentEmailHandler(BaseHandler):
    def get(self, email_id):
        email = Email.get_by_id(int(email_id))
        params = {"email": email}
        return self.render_template("sent-details.html", params)


class DeleteSentEmailHandler(BaseHandler):
    def get(self, email_id):
        email = Email.get_by_id(int(email_id))
        params = {"email": email}
        return self.render_template("delete.html", params)

    def post(self, email_id):
        email = Email.get_by_id(int(email_id))
        email.deleted = True
        email.put()
        return self.redirect("/sent")

class DeleteReceivedEmailHandler(BaseHandler):
    def get(self, email_id):
        email = Email.get_by_id(int(email_id))
        params = {"email": email}
        return self.render_template("delete.html", params)

    def post(self, email_id):
        email = Email.get_by_id(int(email_id))
        email.deleted = True
        email.put()
        return self.redirect("/received")


class WeatherHandler(BaseHandler):
    def get(self):
        url = "http://api.openweathermap.org/data/2.5/weather?q=Celje,si&units=metric&APPID=0fa4f697d72b1a4616a02c99f798df9c"
        result = urlfetch.fetch(url)
        data = json.loads(result.content)
        params = {"data": data}
        return self.render_template("weather.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/loading', LoadingHandler),
    webapp2.Route('/received', ReceivedHandler),
    webapp2.Route('/received-details/<email_id:\d+>', EachReceivedEmailHandler),
    webapp2.Route('/sent', SentHandler),
    webapp2.Route('/sent-details/<email_id:\d+>', EachSentEmailHandler),
    webapp2.Route('/weather', WeatherHandler),
    webapp2.Route('/delete/<email_id:\d+>', DeleteSentEmailHandler),
    webapp2.Route('/received-details/<email_id:\d+>/delete', DeleteReceivedEmailHandler),
], debug=True)
