from graphqlclient import GraphQLClient
graphQLClient = GraphQLClient('http://localhost:4444/')

def getSteamGame(appID):
    steam_game = graphQLClient.execute('''
    query Game($appID: String!){
                    Game(appID: $appID) {
                                        name
                                        appID
                                        genres
                                        tags
                                        averagePlaytime
                                        medianPlaytime
                                        userscore
                                        developer
                                        publisher
                                        rating {
                                            positive
                                            negative
                                        }
                                        ccu
                                        price
                                        timeToBeat {
                                            hastly
                                            normally
                                            completely
                                        }
                                        gameEngines
                                        themes
                                        keywords
                                        releaseDate
                                        minimumAge
                                        }
                    }
''', variables={"appID":appID})
    return steam_game

def predictSteamGame(classifier, transformed_game_dataframe):
    return classifier.predict(transformed_game_dataframe)