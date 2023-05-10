from flask import Flask
from .app import *

def create_app():
    app = Flask(__name__)
    