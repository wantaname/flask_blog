from flask import Flask
import write,category,blogs,read,timeline,user
from flask_cors import CORS
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('settings.py', silent=True)
    CORS(app, resources=r'/*')
    app.register_blueprint(write.bp)

    app.register_blueprint(category.bp)
    app.register_blueprint(blogs.bp)
    app.register_blueprint(read.bp)
    app.register_blueprint(timeline.bp)
    app.register_blueprint(user.bp)

    return app
app=create_app()


