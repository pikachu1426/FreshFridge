import webapp2
import os
import jinja2

current_jinja_environment = JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello")











app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/', HomeHandler)
])
