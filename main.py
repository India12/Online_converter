#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


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
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")
    def post(self):
        first_number = float(self.request.get("first_number"))
        selected_unit = self.request.get("unitlist")

        if selected_unit == "km":
            second_num = str(km_to_miles(first_number)) + "  miles"
        elif selected_unit == "miles":
            second_num = str(miles_to_km(first_number)) + "  kilometers"

        params = {"first_number": first_number, "selected_unit": selected_unit, "second_num": second_num}

        return self.render_template("main.html", params=params) 


def km_to_miles(km):
    miles = km * 0.621371
    return miles

def miles_to_km(miles):
    km = miles * 1.60934
    return km


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
