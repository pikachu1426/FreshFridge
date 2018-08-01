import webapp2
import json
import os
import jinja2
import datetime
import time
from food_items import FoodItem
from food_items import User
from google.appengine.ext import ndb
from google.appengine.api import users


f = open('client_secret.json', 'r')
client_secrets =json.loads(f.read())
f.close()



current_jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

current_food_information = {}

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = current_jinja_environment.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())



class LoginHandler(webapp2.RequestHandler):
    def get(self):
        loggedin_user = users.get_current_user()

        if loggedin_user:
            current_users = User.query(User.id == loggedin_user.user_id()).fetch()
            self.response.write(current_users)
            x = []
            if current_users == x:
                template = current_jinja_environment.get_template('templates/signup.html')
                self.response.write(template.render())
            else:
                template = current_jinja_environment.get_template('templates/home.html')
                self.response.write(template.render({'logout_link': users.create_logout_url('/')}))
        else:
            login_prompt_template = current_jinja_environment.get_template('templates/login.html')
            self.response.write(login_prompt_template.render({'login_link': users.create_login_url('/')}))


class MakeUserHandler(webapp2.RequestHandler):
    def post(self):
        user = User(first_name = self.request.get('name'), id = users.get_current_user().user_id())
        user.put()
        time.sleep(.25)
        self.redirect('/homepage')



class AddFoodHandler(webapp2.RequestHandler):
    def post(self):
        template_vars= {
        'client_id':client_secrets['web']['client_id'],
        'api_key':client_secrets['web']['api_key'],
        }
        food_template = current_jinja_environment.get_template('/templates/food.html')

        self.response.write("You made it to Add Food")
        self.response.write(food_template.render(template_vars))



class FoodConfirmHandler(webapp2.RequestHandler):
    def post(self):
        template_vars = {
            'food_type': self.request.get('food-type'),
            'food_name': self.request.get('food-name'),
            'bought_date': self.request.get('bought-date'),
            'exp_date': self.request.get('exp-date'),
        }

        current_food_information['food_type'] = self.request.get('food-type')
        current_food_information['food_name'] = self.request.get('food-name')
        current_food_information['bought_date'] = self.request.get('bought-date')
        current_food_information['exp_date'] = self.request.get('exp-date')
        confirm_template = current_jinja_environment.get_template('/templates/confirm.html')

        self.response.write(confirm_template.render(template_vars))


#class ConfirmedHandler(webapp2.RequestHandler):
class ConfirmedHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write("Food Item Added to Database")
        bought_date_list = current_food_information['bought_date'].split('/')
        exp_date_list = current_food_information['exp_date'].split('/')

        FoodItem(user_id=str(users.get_current_user().user_id()), food_type=current_food_information['food_type'], food_name=current_food_information['food_name'],\
            buy_month=int(bought_date_list[0]), buy_date=int(bought_date_list[1]), buy_year=int(bought_date_list[2]),\
            exp_month=int(exp_date_list[0]), exp_date=int(exp_date_list[1]), exp_year=int(exp_date_list[2])).put()
        confirmed_template = current_jinja_environment.get_template('/templates/confirmed.html')
        self.response.write(confirmed_template.render())

class ListFoodHandler(webapp2.RequestHandler):
    def get(self):
        food_item_query = FoodItem.query().filter(FoodItem.user_id==str(users.get_current_user().user_id()))
        food_list_dict = {'get_list': ''}
        for food_item in food_item_query:
            str_temp = "<tr>"
            str_temp+=('<td>'+food_item.food_type+'</td>')
            str_temp+=('<td>'+food_item.food_name+'</td>')
            now_time = datetime.datetime.now()
            bought_time = datetime.datetime(food_item.buy_year, food_item.buy_month, food_item.buy_date)
            exp_time = datetime.datetime(food_item.exp_year, food_item.exp_month, food_item.exp_date)
            str_temp+=('<td>'+str(food_item.buy_month)+'/'+str(food_item.buy_date)+'/'+str(food_item.buy_year)+'</td>')
            str_temp+=('<td>'+str(food_item.exp_month)+'/'+str(food_item.exp_date)+'/'+str(food_item.exp_year)+'</td>')
            if now_time>=exp_time or bought_time>=exp_time:
                str_temp+=('<td>'+str(True)+'</td>')
            else:
                str_temp+=('<td>'+str(False)+'</td>')
            str_temp+=("<td><form method='post' action='/remove'> <input type='hidden' name='food_item_key' value=" + str(food_item.key.id()) + "><input type='submit' value='Remove' ></form></td>")
            str_temp+='</tr>'
            food_list_dict['get_list']+=str_temp



        list_template = current_jinja_environment.get_template('/templates/listFood.html')
        self.response.write(list_template.render(food_list_dict))





class RemoveHandler(webapp2.RequestHandler):
    def post(self):
        food_item_key = self.request.get('food_item_key')
        for item in FoodItem.query():
            if str(item.key.id())==food_item_key:
                item.key.delete()
        delete_template = current_jinja_environment.get_template('/templates/delete.html')
        self.response.write(delete_template.render())













app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/', WelcomeHandler),
    ('/login-page', LoginHandler),
    ('/make-user', MakeUserHandler),
    ('/add-food', AddFoodHandler),
    ('/list-food', ListFoodHandler),
    ('/confirm', FoodConfirmHandler),
    ('/confirmed', ConfirmedHandler),
    ('/remove', RemoveHandler),
])
