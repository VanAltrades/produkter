from flask import Flask

app = Flask(__name__)

class MyRoutes:
    def __init__(self):
        pass

    @app.route('/')
    def home(self):
        return 'Home Page'

    @app.route('/about')
    def about(self):
        return 'About Page'

    @app.route('/contact')
    def contact(self):
        return 'Contact Page'

# Create an instance of MyRoutes
my_routes_instance = MyRoutes()

# Use the instance methods as routes
app.add_url_rule('/', view_func=my_routes_instance.home)
app.add_url_rule('/about', view_func=my_routes_instance.about)
app.add_url_rule('/contact', view_func=my_routes_instance.contact)

if __name__ == '__main__':
    app.run(debug=True)