import os

from backend.app import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))


if __name__ == '__main__':
    app.run()
