import webapp2
import os
import jinja2

current_jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        home_template = current_jinja_environment.get_template('/templates/home.html')
        self.response.write(home_template.render())


class AddFoodHandler(webapp2.RequestHandler):
    def post(self):
        food_template = current_jinja_environment.get_template('/templates/food.html')

        self.response.write("You made it to Add Food")
        self.response.write(food_template.render())


class FoodConfirmHandler(webapp2.RequestHandler):
    def post(self):
        
        template_vars = {
            'food-type': self.request.get('food-type'),
            'food-name': self.request.get('food-name'),
        }
        confirm_template = currentjinia_environment.get_template('/templates/confirm.html')

        self.response.write(confirm_template.render())



class ListFoodHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write("You made it to List Food")





class AddEvent(webapp2.RequestHandler):
    def get(self):
        self.response.write(" Add Event Here.")





app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/', HomeHandler),
    ('/add-food', AddFoodHandler),
    ('/list-food', ListFoodHandler),
    ('/confirm', FoodConfirmHandler)
])
