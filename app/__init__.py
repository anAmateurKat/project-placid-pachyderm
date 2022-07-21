from crypt import methods
from email.policy import default
import os
from datetime import datetime
from sqlite3 import Time
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import * 
from peewee import fn
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)


# Connect to MySQL database
# Want to use an in-memory instance of the database when executing tests so 
# that our tests are not dependent upon a separate mysql instance. 
# We can do this by setting the mydb variable to an in-memory sqlite 
# database during testing.
#
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                        user=os.getenv("MYSQL_USER"),
                        password=os.getenv("MYSQL_PASSWORD"),
                        host=os.getenv("MYSQL_HOST"),
                        port=3306)

print(mydb)

# public timeline to post updates in school & career journey
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])
 

# variables
class Hobby:
    def __init__(self, img_url, title, description):
        self.img_url = img_url
        self.title = title
        self.description = description


my_hobbies = [Hobby('https://picsum.photos/id/217/200/300', 'Recipe Development', 'I make the coolest foods :))'),
                Hobby('https://picsum.photos/id/27/200/300', 'Biking', 'Bike is life! 🚵🚵🚵'),
                Hobby('https://picsum.photos/id/238/200/300', 'Reading', 'Reading transports me into a world no one else has seen or will ever see') ]

class Education:
    def __init__(self, school_name, grad_year, description):
        self.school_name = school_name
        self.grad_year = grad_year
        self.description = description

my_education = [Education('Current School', 'Graduation year', 'brief  description of your program of study, major and the like... Est iure fugit in nulla officia hic delectus quia qui veniam voluptas vel consequuntur placeat qui esse dignissimos aut tempora laudantium! Aut repellat doloremque aut quod dolores ut repellat iusto quo nihil aperiam ut animi maxime et quia dolor.'),
                Education('Previous School', 'Graduation year', 'brief  description of your program of study, major and the like... Est iure fugit in nulla officia hic delectus quia qui veniam voluptas vel consequuntur placeat qui esse dignissimos aut tempora laudantium! Aut repellat doloremque aut quod dolores ut repellat iusto quo nihil aperiam ut animi maxime et quia dolor.')]

class Experience:
    def __init__(self, experience_name, description):
        self.experience_name = experience_name
        self.description = description

my_experiences = [Experience('Title1', 'description of your working experience... Est iure fugit in nulla officia hic delectus quia qui veniam voluptas vel consequuntur placeat qui esse dignissimos aut tempora laudantium! Aut repellat doloremque aut quod dolores ut repellat iusto quo nihil aperiam ut animi maxime et quia dolor.'),
                 Experience('Title2', 'description of your working experience... Est iure fugit in nulla officia hic delectus quia qui veniam voluptas vel consequuntur placeat qui esse dignissimos aut tempora laudantium! Aut repellat doloremque aut quod dolores ut repellat iusto quo nihil aperiam ut animi maxime et quia dolor.')]

my_additional_experiences = [Experience('Title1', 'description of volunteer work, hackathons etc... Est iure fugit in nulla officia hic delectus quia qui veniam voluptas vel consequuntur placeat qui esse dignissimos aut tempora laudantium! Aut repellat doloremque aut quod dolores ut repellat iusto quo nihil aperiam ut animi maxime et quia dolor.'),
                            Experience('Title2', 'description of volunteer work, hackathons etc... Est iure fugit in nulla officia hic delectus quia qui veniam voluptas vel consequuntur placeat qui esse dignissimos aut tempora laudantium! Aut repellat doloremque aut quod dolores ut repellat iusto quo nihil aperiam ut animi maxime et quia dolor.')]


class Project:
    def __init__(self, img_url, title, description):
        self.img_url = img_url
        self.title = title
        self.description = description

my_projects = [Project('https://picsum.photos/id/17/200/300', 'Code the World', 'Super awesome project that I cannot wait to share with everyone! Making this change to test redeploy for part C of week 7 LMS.'),
                Project('https://picsum.photos/id/200/200/300','Amazing Glace', 'Glaciers are awesome! 😍 Check out the world\'s coolest glaciers through this interactive game.'),
                Project('https://picsum.photos/id/110/200/300', 'KiKi\'s Delivery App', 'Everything delivered fast & furious.')]

class Location:
    def __init__(self, id, loc, img_urls, title, description):
        self.id = id
        self.loc = loc
        self.img_urls = img_urls
        self.title = title
        self.description = description

my_locations = [Location('van',[43.75, 79.87],['https://picsum.photos/id/17/200/300'],'Vancouver, BC', 'my beautiful home <3'),
                Location('ham',[45.75, 70.87],['https://picsum.photos/id/200/200/300'],'Hamilton, ON', 'where I went to Shad, my first ever tech experience'),
                Location('otw',[66.75, 105.87],['https://picsum.photos/id/110/200/300'],'Ottawa, ON', 'just magnificent')]

@app.route('/')
@app.route('/index.html')
def index():
   return render_template('index.html', title="About Me", firstname="Placid", lastname="Akat", url=os.getenv("URL"))

@app.route('/hobbies.html')
def hobbies():
    return render_template('hobbies.html', title="Hobbies",hobbies=my_hobbies, locations=my_locations)


@app.route('/experiences.html')
def experiences():
    return render_template('experiences.html', title="My Experiences", education=my_education, experiences=my_experiences, add_experiences=my_additional_experiences)

@app.route('/projects.html')
def projects():
    return render_template('projects.html', title="Projects", projects=my_projects)

@app.route('/timeline.html')
def timelineposts(): 
    return render_template('timeline.html', title="Timeline")

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    if 'name' not in request.form:
        return "Error. Request missing the field 'name'", 400
    if 'email' not in request.form:
        return "Error. Request missing the field 'email'", 400
    if 'content' not in request.form:
        return "Error. Request missing the field 'content'", 400
  
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    
    if name == "":
        return "Error. Name should not be empty", 400
    if email == "":
        return "Error. Email should not be empty", 400
    if "@" not in email:
        return "Error. Invalid email", 400
    if content == "":
        return "Error. Content should not be empty", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post(): 
    return{
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post(): 
    #Model.select(#fields) returns ModelSelect query 
    #Model.get(*query, **filters) returns a single model instance matching the specified filters

    #* need to handle case where DB table is empty 
    subq = TimelinePost.select(fn.MAX(TimelinePost.created_at)).scalar() 
    row_to_del = TimelinePost.get(TimelinePost.created_at == subq)
    row_to_del.delete_instance()

    return{
        'deleted': 
            model_to_dict(row_to_del)
    }

if __name__ == "__main__":
    app.run(debug=True)
 
