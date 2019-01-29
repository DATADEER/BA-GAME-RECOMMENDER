
#TRANSOFORMERS CONVERT RAW DATA INTO DATA THAT IS CONSUMABLE BY THE CLASSIFIER
import pandas
from datetime import date
from modules.utility import removeTrailingZero
import numpy

def transformDBResultForTraining(single_game_result):

    return {
        "appid": single_game_result["Game"]["appID"],
        "name": single_game_result["Game"]["name"],
        #"hasMultiplayerSupport": transformBooleanIntoNumber(hasGameMultiplayerSupport(single_game_result)),
        #"hasSingleplayerSupport" : transformBooleanIntoNumber(hasGameSingleplayerSupport(single_game_result)),
        #"hasCoopSupport": transformBooleanIntoNumber(hasGameCoopSupport(single_game_result)),
        "genres": single_game_result["Game"]["genres"],
        "tags": single_game_result["Game"]["tags"],
        "publisher": single_game_result["Game"]["publisher"],
        "developer": replaceEmptyListWithNone(single_game_result["Game"]["developer"]),
        "averagePlaytime": single_game_result["Game"]["averagePlaytime"],
        "medianPlaytime": single_game_result["Game"]["medianPlaytime"],
        "userscore": single_game_result["Game"]["userscore"],
        "rating": calculatePositiveRating(single_game_result["Game"]["rating"]),
        "ccu": single_game_result["Game"]["ccu"],
        "price": tranformPriceForTraining(single_game_result["Game"]["price"]),
        "timeToBeatHastly": single_game_result["Game"]["timeToBeat"]["hastly"],
        "timeToBeatNormally": replaceNoneWith0(single_game_result["Game"]["timeToBeat"]["normally"]),
        "timeToBeatCompletely": single_game_result["Game"]["timeToBeat"]["completely"],
        "gameEngines": single_game_result["Game"]["gameEngines"],
        "themes": single_game_result["Game"]["themes"],
        "releaseYear": extractYearFromTimestamp(single_game_result["Game"]["releaseDate"]),
        "minimumAge": replaceNoneWith12(removeTrailingZero(single_game_result["Game"]["minimumAge"]))
    }

def getIndexesOfGamesMissingValue(games,column_title):

    print(len(games))
    print(games.iterrows())
    game_indexes = []
    for i,(index, game) in enumerate(games.iterrows()):
        if game[column_title] == None or not game[column_title] or None or game[column_title] == "":
            print(game["name"],"(",index,")",i)
            game_indexes.append(index)
    return game_indexes

def getIndexesOfBetaTestGames(games):

    irrelevant_games_indicators = ["public test","closed test", "closed beta", "closed alpha","public alpha", "player profile", "balance beta", "obsolete", "(beta)", "(alpha)","staging branch", "test server"]
    game_indexes = []
    for index, game in games.iterrows():
        if any(word in game["name"].lower() for word in irrelevant_games_indicators):
            print(game["name"])
            game_indexes.append(index)
    return game_indexes

def getOwnedGamesIndexes(owned_games, games):
    owned_games_appids = [game["appid"] for i,game in owned_games.iterrows()]
    owned_games_indexes = []
    for index, game in games.iterrows():
        if any(index in game["appid"] for index in owned_games_appids):
            owned_games_indexes.append(index)
    return owned_games_indexes


def removeGamesFromFeaturesAndLabels(game_indexes, features, labels):
    print("will remove indexes", game_indexes)
    cleaned_features = features.drop(game_indexes, axis=0)
    cleaned_labels = numpy.delete(labels, game_indexes)
    return {"features": cleaned_features, "labels": cleaned_labels}

def removeGamesFromFeatures(game_indexes, features):
    return features.drop(game_indexes, axis=0)


def extractYearFromTimestamp(timestamp):
    if(timestamp != None):
        timestamp = int(timestamp)
        return removeTrailingZero(date.fromtimestamp(timestamp/1000.0).year)
    else:
        return None


def calculatePositiveRating(rating):
    if(rating["positive"] != None or rating["negative"] != None):
        sumOfRatings = rating["positive"] + rating["negative"]
        if(sumOfRatings == 0):
            return 0
        else:
            return removeTrailingZero(round((rating["positive"] / sumOfRatings) * 100, 0))

    else:
        return 0

def replaceEmptyListWithNone(value):
    if(not value):
        return None
    else:
        return value

def replaceNoneWith12(value):
    if(value == None or value == "None"):
        return 12
    else:
        return removeTrailingZero(value)

def replaceNoneWithYear(value):
    if(value == None):
        return 0
    else:
        return removeTrailingZero(value)

def replaceNoneWith0(value):
    if(value == None):
        return 0
    else:
        return removeTrailingZero(value)

def replace0WithNone(value):
    if(value == 0):
        return None
    else:
        return removeTrailingZero(value)

def categorize_price(price):
    if (price == 0):
        return 0
    elif (round(price, 0) > 0 and round(price, 0) <= 100):
        return 1
    elif (round(price, 0) > 100 and round(price, 0) <= 500):
        return 5
    elif (round(price, 0) > 500 and round(price, 0) <= 1000):
        return 10
    elif (round(price, 0) > 1000 and round(price, 0) <= 1500):
        return 15
    elif (round(price, 0) > 1500 and round(price, 0) <= 2500):
        return 25
    elif (round(price, 0) > 2500 and round(price, 0) <= 3500):
        return 35
    elif (round(price, 0) > 3500 and round(price, 0) <= 4000):
        return 40
    elif (round(price, 0) > 4000 and round(price, 0) <= 5000):
        return 50
    elif (round(price, 0) > 5000 and round(price, 0) <= 6000):
        return 60
    else:
        return 70

def doesGameSupportThisCategory(single_game, category_id):
    try:
        matching_categories = list(filter((lambda category: int(category["id"]) == int(category_id)), single_game["categories"]))
        if (len(matching_categories) > 0):
            return True
        else:
            return False
    except:
        return False

def transformBooleanIntoNumber(boolean):
    if(boolean == True):
        return 1
    else:
        return 0

def hasGameSingleplayerSupport(single_game):
    singleplayer_category_id = 2
    return doesGameSupportThisCategory(single_game,singleplayer_category_id)

def hasGameMultiplayerSupport(single_game):
    multiplayer_category_id = 1
    return doesGameSupportThisCategory(single_game, multiplayer_category_id)

def hasGameOnlineMultiplayerSupport(single_game):
    coop_category_id = 36
    return doesGameSupportThisCategory(single_game, coop_category_id)

def hasGameCoopSupport(single_game):
    coop_category_id = 9
    return doesGameSupportThisCategory(single_game, coop_category_id)

def hasGameOnlineCoopSupport(single_game):
    coop_category_id = 38
    return doesGameSupportThisCategory(single_game, coop_category_id)

def tranformPriceForTraining(price):
    if (price == True or price == 0 or price == None):
        return 0
    elif (price):
        price = int(price)
        return categorize_price(price)
    else:
        return None

def tranformRecommendationsForTraining(single_game_result):
    try:
        return single_game_result["recommendations"]["total"]
    except TypeError:
        return 0

def tranformGenresForTraining(single_game_result):
    try:
        return list(map(lambda genre: genre["id"], single_game_result["genres"]))
    except TypeError:
        return 0

def tranformPublishersForTraining(single_game_result):
    try:
        return single_game_result["publishers"][0]
    except TypeError:
        return "Unknown"

def tranformDevelopersForTraining(single_game_result):
    try:
        return single_game_result["developers"][0]
    except TypeError:
        return "Unknown"

def transformSimpleCategoricalDataForTraining(game_data_frame, categorical_features):
    return pandas.get_dummies(game_data_frame, columns=categorical_features)

def transformComplexCategoricalFeatureForTraining(game_data_frame, categorical_feature):
    transformed_feature = game_data_frame[categorical_feature].str.join(sep='*').str.get_dummies(sep='*').add_prefix(categorical_feature+"_")
    return pandas.concat([game_data_frame, transformed_feature], axis=1).drop(categorical_feature, axis=1)