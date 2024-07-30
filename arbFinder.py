def arbFinder(odds_json):
    tempList = []

    for game in range(len(odds_json)):
        best = {}
        for bookmaker in range(len(odds_json[game]["bookmakers"])):
            for market in range(len(odds_json[game]["bookmakers"][bookmaker]["markets"])):
                if odds_json[game]["bookmakers"][bookmaker]["markets"][0]["key"] == "h2h":
                    for outcome in range(len(odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"])):
                        if odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome][
                            "name"] not in best:
                            best[odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome]["name"]] \
                                = {odds_json[game]["bookmakers"][bookmaker]["key"]:
                                       odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome][
                                           "price"]}
                        for book in best[
                            odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome]["name"]]:
                            if \
                            best[odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome]["name"]][
                                book] < odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome][
                                "price"]:
                                best[
                                    odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome]["name"]] \
                                    = {odds_json[game]["bookmakers"][bookmaker]["key"]:
                                           odds_json[game]["bookmakers"][bookmaker]["markets"][0]["outcomes"][outcome][
                                               "price"]}
                else:
                    pass
        tempList.append(best)

    bestList = []

    for game in tempList:
        total = 0
        for outcome in game.keys():
            for book in game[outcome]:
                total += 1 / (game[outcome][book])
        if total < .99:
            bestList.append(game)
    return bestList
