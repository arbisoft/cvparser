from flask import Flask
from flask_script import Manager

from management.train_model import TrainModel
from management.label_cvs import LabelCVs
from management import ParseCvSovren, TrainModel, LabelCVs

app = Flask(__name__)

manager = Manager(app)

if __name__ == "__main__":
    manager.add_command('train_model', TrainModel())
    manager.add_command('label_cvs', LabelCVs())
    manager.add_command('parse_cv_sovren', ParseCvSovren())
    manager.run()
