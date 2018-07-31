import webapp2
import json
import os
import jinja2
import datetime
from food_items import FoodItem
from google.appengine.api import users



f = open('client_secret.json', 'r')
client_secrets =json.loads(f.read())
f.close()

print client_secrets

current_jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

current_food_information = {}



class HomeHandler(webapp2.RequestHandler):
    def get(self):
        home_template = current_jinja_environment.get_template('/templates/home.html')
        self.response.write(home_template.render())



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


class ConfirmedHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write("Food Item Added to Database")
        bought_date_list = current_food_information['bought_date'].split('/')
        exp_date_list = current_food_information['exp_date'].split('/')

        FoodItem(food_type=current_food_information['food_type'], food_name=current_food_information['food_name'],\
            buy_month=int(bought_date_list[0]), buy_date=int(bought_date_list[1]), buy_year=int(bought_date_list[2]),\
            exp_month=int(exp_date_list[0]), exp_date=int(exp_date_list[1]), exp_year=int(exp_date_list[2])).put()
        confirmed_template = current_jinja_environment.get_template('/templates/confirmed.html')
        self.response.write(confirmed_template.render())

class ListFoodHandler(webapp2.RequestHandler):
    def post(self):
        food_list_dict = {'get_list': '',}
        food_item_query = FoodItem.query()
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
            str_temp+=("<td><form method='post' action='/list-food'> <input type='submit' value='Remove' ></form></td>")
            str_temp+='</tr>'
            food_list_dict['get_list']+=str_temp

        list_template = current_jinja_environment.get_template('/templates/listFood.html')
        self.response.write(list_template.render(food_list_dict))



















app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/', HomeHandler),
    ('/add-food', AddFoodHandler),
    ('/list-food', ListFoodHandler),
    ('/confirm', FoodConfirmHandler),
    ('/confirmed', ConfirmedHandler),
])
