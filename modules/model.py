from modules.utility import logWithTitle, printSeperator, cPrint, logCommaSeparatedList
from modules.create_model_functions import createFeaturesDataFrame, labelByPredefinedLists
from sample_data.boring_games import boring_games
from sample_data.interesting_games import interesting_games
from modules.transformers import transformDBResultForTraining, transformSimpleCategoricalDataForTraining, transformComplexCategoricalFeatureForTraining
from modules.model_metrics_helper_functions import logOverallPerformance, visualizeClassificationReport, visualizeBestFeatures, logNameOfPredictedGames

from sklearn import svm, model_selection
import numpy
import pandas


def createModel(data):

    #DATA INPUT - GAME DATA & USER DATA
    profile_response = data["user_profile_json"]
    games_response = data["games_json"]
    # FEATURE SELECTION - SELECT FEATURES TO BE USED BY ADDING THEM TO THE features_to_use LIST
    #features_to_use = ["appid","name","genres", "publishers", "developers", "hasMultiplayerSupport", "hasSingleplayerSupport", "hasOnlineMultiplayerSupport"]
    features_to_use = ["appid","name","genres"]

    logWithTitle("USED-FEATURES")
    logCommaSeparatedList(features_to_use)
    cPrint(str(len(features_to_use)) + " Features in Use", "green")

    transformed_games = list(map(transformDBResultForTraining, games_response))

    labels = labelByPredefinedLists(transformed_games, boring_games, interesting_games)
    features = createFeaturesDataFrame(transformed_games, features_to_use)
    #features = transformSimpleCategoricalDataForTraining(features, ["genres","tags"])
    #features = transformComplexCategoricalFeatureForTraining(features, "genres")
    features = transformComplexCategoricalFeatureForTraining(features, "genres")


    #logWithTitle("All-LABELS", labels)
    #logWithTitle("ALL-FEATURES", features)
    #printSeperator()

    #print(len(features))

    features_train_indexes, features_test_indexes, labels_train, labels_test = model_selection.train_test_split(features.index, labels,test_size=0.30)
    features_train_named = features.iloc[features_train_indexes]
    features_test_named = features.iloc[features_test_indexes]
    features_train = features_train_named.drop(["appid","name"], axis=1)
    features_test = features_test_named.drop(["appid","name"], axis=1)

    logWithTitle("DATA SHAPES")
    print(features_train.shape, labels_train.shape, " : ", features_test.shape, labels_test.shape)

    #logWithTitle("Train-Features", features_train)
    #logWithTitle("Test-Features", features_test)
    #logWithTitle("Train-Labels", labels_train)
    #logWithTitle("Test-Labels", labels_test)

    #for game in features_test:
     #   cPrint(game)

    classifier = svm.SVC(kernel="rbf", gamma=1000, C=100.)

    classifier.fit(features_train, labels_train)

    #logWithTitle("PREDICTED LABELS", classifier.predict(features_test))
    #logWithTitle("GROUNDTRUTH LABELS", labels_test)

    logOverallPerformance(classifier, features_test, labels_test)
    # save_classifier("./results/model/SVC.pickle", classifier)

    visualizeClassificationReport(classifier, features_train, labels_train, features_test, labels_test)

    predicted_labels = classifier.predict(features_test)

    logNameOfPredictedGames(predicted_labels, features_test_named)

    #visualizeBestFeatures(features_train, labels_train)
