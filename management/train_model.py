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
        ADDITIONAL_LABELS = ['DEGREE', 'DESIGNATION']
        n_iter = 25

        TRAIN_DATA = [
            ("FAST SCHOOL OF COMPUTER SCIENCE, LAHORE", {"entities": [(0, 4, "ORG"), (15, 31, "DEGREE"), (48, 39, "GPE")]}),
            ("Front desk officer (FDO), FAST University, Lahore", {"entities": [(0, 24, "DESIGNATION"), (26, 30, "ORG")]}),
            ("NATIONAL UNIVERSITY OF COMPUTER & EMERGING SCIENCES (FAST-NU), LAHORE 2013 - 2017",
                {"entities": [(0, 51, "ORG"), (63, 69, "GPE"), (53, 57, "ORG"), (70, 81, "DATE")]}),
            ("Full-Stack Python developer, Arbisoft June 5​th​, 2017 - Present",
                {"entities": [(0, 27, "DESIGNATION"), (29, 37, "ORG"), (38, 54, "DATE")]}),
            ("Intern, Techmaniacs Aug 20​th​, 2016 – Jan 10​th​, 2017",
                {"entities": [(0, 6, "DESIGNATION"), (8, 19, "ORG"), (20, 36, "DATE"), (39, 55, "DATE")]}),
            # ("FAST SCHOOL OF COMPUTER SCIENCE, LAHORE    ● BS in Computer Science",
            #     {"entities": [(0, 4, "ORG"), (15, 31, 'DEGREE'), (45, 67, "DEGREE")]}),
            ("BCS Computer Sciences", {"entities": [(0, 3, 'DEGREE'), (4, 21, "DEGREE")]}),
            ("Superior College ,Sargodha| 2012-2014 ",
                {"entities": [(0, 16, "ORG"), (18, 26, "GPE"), (28, 37, "DATE")]}),
            ("Islamic Alta Vista High School, Sargodha| 2010-2012 ",
                {"entities": [(0, 30, "ORG"), (32, 40, "GPE"), (42, 51, "DATE")]}),
            ("Internship at Techlogix (Pvt) Ltd, Lahore (07/2018 - 08/2018) ",
                {"entities": [(0, 10, "DESIGNATION"), (14, 23, "ORG"), (35, 41, "GPE"), (43, 60, "DATE")]}),
            ("Comsats, ​Lahore — BS ​Computer Engineering ",
                {"entities": [(0, 7, "ORG"), (9, 16, "GPE"), (19, 43, "DEGREE")]}),
            ("Web Developer at Soft Heights (January 2017 to September 2018)",
                {"entities": [(0, 13, "DESIGNATION"), (17, 29, "ORG"), (31, 61, "DATE")]}),
            ("BACHELOR OF IT : University of Education Township",
                {"entities": [(0, 14, "DEGREE"), (17, 40, "ORG"), (41, 49, "GPE")]})
        ]
        model_dir = Path(model)
        if model and model_dir.exists():
            nlp = spacy.load(model)
            print("Loaded model '%s'" % model)
        else:
            nlp = spacy.load('en_core_web_sm')
            print("Created new model")

        # Add entity recognizer to model if it's not in the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if "ner" not in nlp.pipe_names:
            ner = nlp.create_pipe("ner")
            nlp.add_pipe(ner)
        # otherwise, get it, so we can add labels to it
        else:
            ner = nlp.get_pipe("ner")

        for label in ADDITIONAL_LABELS:
            # add new entity label to entity recognizer
            ner.add_label(label)

        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):  # only train NER
            for itn in range(n_iter):
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.upda.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.25,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)

        # Save model
        if not model_dir.exists():
            model_dir.mkdir()
        # nlp.meta["name"] = model  # rename model
        nlp.to_disk(model_dir)
        print("Saved model to", model_dir)
