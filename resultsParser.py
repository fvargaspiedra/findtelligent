#!/usr/bin/env python3


def results_dd(results_list, collection_dictionary):
    for i in results_list:
        collection_dictionary[i[0]][1] = i[1]
    max_list = []
    for element in range(0, len(collection_dictionary)):
        #print(collection_dictionary[element][1])
        # print("For document: " + str(element))
        current = collection_dictionary[element][1]
        if element == 0:
            past = 0
            following = collection_dictionary[element + 1][1]
        elif element == (len(collection_dictionary) - 1):
            following = 0
            past = collection_dictionary[element - 1][1]
        else:
            past = collection_dictionary[element - 1][1]
            following = collection_dictionary[element + 1][1]
        # print("C: " + str(current) + " P: " + str(past) + " F: " + str(following))
        counter = element + 1
        while current == following:
            counter = counter + 1
            if counter >= len(collection_dictionary):
                break
            else:
                following = collection_dictionary[counter][1]
        if (past < current) and (following < current or following == current):
            max_list.append(element)
    return max_list

def results_dd_max_percentage(results_list, collection_dictionary, max_percentage):
    for i in results_list:
        collection_dictionary[i[0]][1] = i[1]
    results = []
    max_scores = []
    max_ids = []
    for element in range(0, len(collection_dictionary)):
        #print(collection_dictionary[element][1])
        # print("For document: " + str(element))
        current = collection_dictionary[element][1]
        if element == 0:
            past = 0
            following = collection_dictionary[element + 1][1]
        elif element == (len(collection_dictionary) - 1):
            following = 0
            past = collection_dictionary[element - 1][1]
        else:
            past = collection_dictionary[element - 1][1]
            following = collection_dictionary[element + 1][1]
        # print("C: " + str(current) + " P: " + str(past) + " F: " + str(following))
        counter = element + 1
        while current == following:
            counter = counter + 1
            if counter >= len(collection_dictionary):
                break
            else:
                following = collection_dictionary[counter][1]
        if (past < current) and (following < current or following == current):
            max_scores.append(collection_dictionary[element][1])
            max_ids.append(element)
    if len(max_ids) != 0:
        max_score_percentage = max(max_scores) * max_percentage * 0.01
        for index, id in enumerate(max_ids):
            if max_scores[index] >= max_score_percentage:
                results.append(id)
        return results
    else:
        return []
