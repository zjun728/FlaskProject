import os

from apps import app  # app为apps包下__init__.py文件声明好的app  app = Flask(__name__)


# print("runserver:",__name__)   #runserver: __main__


if __name__ == '__main__':
    app.run()
