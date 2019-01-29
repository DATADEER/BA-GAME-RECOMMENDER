import matplotlib
#COMMENT OUT matplotlib.use("TkAgg") TO USE INLINE DISPLAY IN JUPYTER NOTEBOOK
#ADD matplotlib.use("TkAgg") TO USE DISPLAY PLOT WHILE USING TERMINAL
#matplotlib.use("TkAgg")
#matplotlib.use("agg")
import matplotlib.pyplot as pyplot
from modules.utility import cPrint, calculateAverage, convertLabelToNumber,logWithTitle
from sklearn.model_selection import cross_val_score, cross_validate
from yellowbrick.classifier import ClassificationReport
from sklearn.ensemble import GradientBoostingClassifier
from yellowbrick.features.importances import FeatureImportances
from yellowbrick.target import ClassBalance
from yellowbrick.model_selection import LearningCurve, CVScores
from yellowbrick.features import Rank2D
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics.scorer import make_scorer
from sklearn.metrics import classification_report
import random

import seaborn


from sklearn import metrics
import numpy

def logCrossValidatedOverallPerformance(classifier, features, labels):

    def precisionInterestingScorer(labels_test, predicted_labels):
        return classification_report(labels_test, predicted_labels, output_dict=True)["1"]["precision"]

    def precisionBoringScorer(labels_test, predicted_labels):
        return classification_report(labels_test, predicted_labels, output_dict=True)["0"]["precision"]

    def recallInterestingScorer(labels_test, predicted_labels):
        return classification_report(labels_test, predicted_labels, output_dict=True)["1"]["recall"]

    def recallBoringScorer(labels_test, predicted_labels):
        return classification_report(labels_test, predicted_labels, output_dict=True)["0"]["recall"]

    scoring = {
        'accuracy': 'accuracy',
        'precision_interesting' : make_scorer(precisionInterestingScorer, greater_is_better=True),
        'precision_boring' : make_scorer(precisionBoringScorer, greater_is_better=True),
        'recall_interesting' : make_scorer(recallInterestingScorer, greater_is_better=True),
        'recall_boring' : make_scorer(recallBoringScorer, greater_is_better=True)
    }
    folds = 10
    scores = cross_validate(classifier, features, list(map(convertLabelToNumber,labels)), scoring=scoring, cv=folds, return_train_score=False,return_estimator=False)
    logWithTitle("CROSS VALIDATED METRICS")

    print("INTERESTING RECALL")
    average_recall_interesting = calculateAverage(scores["test_recall_interesting"])
    cPrint(round(average_recall_interesting, 2), color="red")

    print("INTERESTING PRECISION")
    average_precision_interesting = calculateAverage(scores["test_precision_interesting"])
    cPrint(round(average_precision_interesting, 2),color="green")
    #print(scores["test_precision_interesting"])
    #print(numpy.var(scores["test_precision_interesting"]))

    print("BORING RECALL")
    average_recall_boring = calculateAverage(scores["test_recall_boring"])
    cPrint(round(average_recall_boring, 2), color="red")

    print("BORING PRECISION")
    average_precision_boring = calculateAverage(scores["test_precision_boring"])
    cPrint(round(average_precision_boring, 2), color="green")

    print("ACCURACY")
    average_precision_boring = calculateAverage(scores["test_accuracy"])
    cPrint(round(average_precision_boring, 2))




def getOverallPerformance(classifier, features_test, labels_test):

    predicted_labels = classifier.predict(features_test)
    labels_test = numpy.asarray(labels_test)
    folds = 10
    scores = cross_val_score(classifier, features_test, labels_test, cv=folds)
    print(scores)
    accuracy_score = sum(scores)/folds
    #accuracy_score = metrics.accuracy_score(labels_test, predicted_labels)
    classification_report = metrics.classification_report(labels_test, predicted_labels)

    return {
        "accuracy_score": accuracy_score,
        "classification_report": classification_report
    }

def logOverallPerformance(classifier, features_test, labels_test):

    performanceObject = getOverallPerformance(classifier, features_test, labels_test)

    print("ACCURACY SCORE:")
    cPrint(performanceObject["accuracy_score"],"green")
    #print("CLASSIFICATION REPORT:")
    #cPrint(performanceObject["classification_report"],"green")


def visualizeClassificationReport(classifier, features_train, labels_train, features_test, labels_test):

    visualizer = ClassificationReport(classifier)

    visualizer.fit(features_train, labels_train)
    visualizer.score(features_test, labels_test)
    visualizer.poof()

def visualizeBestFeatures(features_train, labels_train):

    figure = pyplot.figure()
    ax = figure.add_subplot()

    visualization = FeatureImportances(GradientBoostingClassifier(), ax=ax)
    visualization.fit(features_train, labels_train)
    visualization.poof()

def getGameRecommendations(predicted_labels, features_named, number_of_recommendations = 3):

    predicted_as_interesting = getNameOfPredictedGames(predicted_labels, features_named)["interesting_games"]

    #TODO: Refactor shuffle and pop because its manipulating "global" state
    if(len(predicted_as_interesting) >= number_of_recommendations):
        selected_games =[]
        for item_number in range(number_of_recommendations):
            random.shuffle(predicted_as_interesting)
            selected_game = predicted_as_interesting.pop()
            selected_games.append(selected_game)
        return selected_games
    else:
        return predicted_as_interesting

def getNameOfPredictedGames(predicted_labels, features_named):

    interesting_games = []
    boring_games = []
    unknown_games = []
    for index, prediction in enumerate(predicted_labels):
        if(prediction == "interesting"):
            interesting_games.append(features_named.iloc[index]["name"])
        elif(prediction == "boring"):
            boring_games.append(features_named.iloc[index]["name"])
        else:
            unknown_games.append(features_named.iloc[index]["name"])
            cPrint(str(features_named.iloc[index]["name"]) + " has no label. investigate further", color="yellow")
    return {"interesting_games":interesting_games,"boring_games":boring_games,"unknown_games":unknown_games}


def logNameOfPredictedGames(predicted_labels, features_named):

    for index, prediction in enumerate(predicted_labels):
        if(prediction == "interesting"):
            cPrint(features_named.iloc[index]["name"],color="green")
        elif(prediction == "boring"):
            cPrint(features_named.iloc[index]["name"], color="red")
        else:
            cPrint(str(prediction) + " can't be found in any list", color="yellow")


def visualizeClassImbalance(labels_train, lables_test=None):
    visualizer = ClassBalance(labels=["boring", "interesting"])
    visualizer.fit(labels_train, lables_test)
    visualizer.poof()

def visualizeLearningCurve(classifier, features, labels, scoring='precision'):

    sizes = numpy.linspace(0.1, 1.0, 10)
    cv = StratifiedKFold(10)
    visualizer = LearningCurve(
        classifier, cv=cv, train_sizes=sizes,
        scoring=scoring, n_jobs=10
    )

    visualizer.fit(features.drop(["appid", "name"], axis=1), list(map(convertLabelToNumber, labels)))
    visualizer.poof()

def visualizeKFoldCrossValidation(classifier, features, labels):

    cv = StratifiedKFold(10)
    # Create the cv score visualizer
    oz = CVScores(
        classifier, cv=cv, scoring='precision'
    )

    oz.fit(features.drop(["appid", "name"], axis=1), list(map(convertLabelToNumber, labels)))
    oz.poof()

def visualizeFeatureImportance(features, labels):

    # Instantiate the visualizer with the Covariance ranking algorithm
    visualizer = Rank2D(algorithm='covariance')

    visualizer.fit(features.drop(["appid", "name"], axis=1), list(map(convertLabelToNumber, labels)))  # Fit the data to the visualizer
    visualizer.transform(features.drop(["appid", "name"], axis=1))  # Transform the data
    visualizer.poof()  # Draw/show/poof the data



