import numpy
import pandas

def getPlaytime(user_games_with_playtime, appid):
    matchingGames = list(filter(lambda game: str(game["appid"]) == appid, user_games_with_playtime))
    if(len(matchingGames) >= 1):
        return matchingGames[0]["playtime_forever"]
    else:
        return False

def createFeaturesDataFrame(transformed_games, features_to_use):
    return pandas.DataFrame(data=transformed_games, columns=features_to_use)


def calculateManualLabel(playtime):
    if (playtime < 60):
        return "boring"
    else:
        return "interesting"

def calculateAllLabels(transformed_games, profile_response):

    game_labels = []
    for game in transformed_games:
        #print("playtime")
        #print((getPlaytime(profile_response["games"]["list"], game["appid"])))
        manually_determined_lable = calculateManualLabel(getPlaytime(profile_response["games"]["list"], game["appid"]))
        game_labels.append(manually_determined_lable)

    return game_labels

def labelByPredefinedLists(transformed_games, boring_games, interesting_games):
    game_labels = []
    for game in transformed_games:
        if(game["appid"] in interesting_games):
            game_labels.append("interesting")
        elif(game["appid"] in boring_games):
            game_labels.append("boring")
        else:
            print("there is no class defined for gameID: " + str(game["appid"]))
            game_labels.append("boring")

    return numpy.asarray(game_labels)

