from flask import Flask
from app import ServerFunctions, create_app  

if __name__ == '__main__':
    app_instance = create_app()
    app_instance.app.run(debug=True)