import random
import spacy
from pathlib import Path
from flask_script import Command, Option
from spacy.util import minibatch, compounding


class TrainModel(Command):
    """Train model based on data provided."""

    option_list = (
        Option('--model', '-m', dest='model'),
    )

    def run(self, model):
        n_iter = 25
        TRAIN_DATA = [
            ("FAST University Lahore", {"entities": [(16, 22, "GPE")]}),
            ("FAST University LAHORE", {"entities": [(16, 22, "GPE")]}),
            ("I live in Lahore, Pakistan.", {"entities": [(10, 15, "LOC"), (17, 25, "LOC")]}),
        ]
        model_dir = Path(model)
        if model and model_dir.exists():
            nlp = spacy.load(model)  # load existing spaCy model
            print("Loaded model '%s'" % model)
        else:
            nlp = spacy.load('en_core_web_sm')
            print("Created new model")

        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.25,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

        # save model to output directory
        if not model_dir.exists():
            model_dir.mkdir()
        # nlp.meta["name"] = model  # rename model
        nlp.to_disk(model_dir)
        print("Saved model to", model_dir)
