import webapp2
import os
import jinja2

current_jinja_environment = JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/home.html')
        self.response.write(welcome_template.render())












app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/', HomeHandler)
])
