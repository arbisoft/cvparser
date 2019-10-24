from flask import Flask
from flask_script import Manager

from management.train_model import TrainModel

app = Flask(__name__)

manager = Manager(app)

if __name__ == "__main__":
    manager.add_command('train_model', TrainModel())
    manager.run()
