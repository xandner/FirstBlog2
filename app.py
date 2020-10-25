from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Development
from flask_migrate import Migrate
from redis import Redis
# import views


app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
redis=Redis.from_url(app.config['REDIS_SERVER_URL'])
from mod_users import users

from views import hello_world

from mod_admin import admin
from  mod_blog import blog
from mod_uploads import uploads

app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(blog)
app.register_blueprint(uploads)
if __name__ == '__main__':
    app.run()
