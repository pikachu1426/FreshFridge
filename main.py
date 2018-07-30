import webapp2
import os
import jinja2

current_jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, welcome to FreshFridge!")
        home_template = current_jinja_environment.get_template('/templates/home.html')
        self.response.write(home_template.render())





class AddEvent(webapp2.RequestHandler):
    def get(self):
        self.response.write(" Add Event Here.")





app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/', HomeHandler)
])
