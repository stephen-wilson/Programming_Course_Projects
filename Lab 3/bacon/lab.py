#!/usr/bin/env python3

from cgitb import small
from importlib.resources import path
import pickle
import queue
from tracemalloc import start

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    """
    Transform the data to a social network graph data structure.
    The graph should have edges in a set with tuples representing an
    edge from one node (actor) to another. (a,b) = (b,a) so a set data structure works.
    Furthermore, the film they acted in doesn't matter, so that can be dropped.
    """
    transformed_data = {}
    for actor1, actor2, film in raw_data:
        # add both in reciprocally
        if actor1 in transformed_data:
            # add actor AND the film they acted in together
            transformed_data[actor1][actor2] = film
        else:
            # store dictionary with actors as keys and films they acted in together as elements
            transformed_data[actor1] = {actor2: film}
        if actor2 in transformed_data:
            transformed_data[actor2][actor1] = film
        else:
            transformed_data[actor2] = {actor1: film}
            
    return transformed_data


def acted_together(transformed_data, actor_id_1, actor_id_2):
    
    if actor_id_1 == actor_id_2:
       return actor_id_1 in transformed_data 
   
    return actor_id_1 in transformed_data and actor_id_2 in transformed_data[actor_id_1]
    
    
    
    
def actors_with_bacon_number(transformed_data, n):
    """
    Given the transformed data (graph), calculates the actors
    which have the shortest path of length n to Mr. Bacon.
    
    Returns:
    actors_with_bacon_num (set): actor IDs with bacon number as described above
    """
    baconID = 4724
    
    # acted_with_bacon = transformed_data[baconID]['actors']
    acted_with_bacon = set(transformed_data[baconID].keys())
    bacon_num_actors = [acted_with_bacon]
    visited = acted_with_bacon.copy()
    visited.add(baconID)
    
    if acted_with_bacon and n > 0:
        if n == 1:
            return acted_with_bacon
        i = 1
        while i < n and bacon_num_actors[i-1]:
            # actors_to_add = set()
            for prev_actor in bacon_num_actors[i-1]:
                # get all the actors on this level (bacon num level)
                if len(bacon_num_actors) <= i:
                    bacon_num_actors.append(set())
                for actor in transformed_data[prev_actor]:
                    if actor not in visited:
                        # temp_actors.add(actor)
                        bacon_num_actors[i].add(actor)
                        visited.add(actor)
            i += 1
        if not bacon_num_actors[i-1]:
            return set()
    else:
        return {baconID}
    
    return bacon_num_actors[n-1]

def find_path(transformed_data, goal_actor = None, start_id=4724, goal_test_function = None):
    if goal_actor == start_id or (goal_test_function and goal_test_function(start_id)):
        return [start_id]
    
    paths = {}
    
    acted_with_start_actor = set(transformed_data[start_id].keys())
    bacon_num_actors = [acted_with_start_actor]
    visited = acted_with_start_actor.copy()
    visited.add(start_id)
    for actor in acted_with_start_actor:
        paths[actor] = [start_id, actor]
    
    
    # current_actor = start_id
    if acted_with_start_actor:       
        i = 1 
        while goal_actor not in paths and bacon_num_actors[i-1]:
            # actors_to_add = set()
            for prev_actor in bacon_num_actors[i-1]:
                # get all the actors on this level (bacon num level)
                if len(bacon_num_actors) <= i:
                    bacon_num_actors.append(set())
                for actor in transformed_data[prev_actor]:
                    if actor not in visited:
                        bacon_num_actors[i].add(actor)
                        visited.add(actor)
                        if goal_test_function and goal_test_function(actor):
                            goal_actor = actor
                        # keep track of the paths to each actor from bacon levels
                        if prev_actor in paths:
                            temp_copy = paths[prev_actor].copy()
                            temp_copy.append(actor)
                            paths[actor] = temp_copy
            i += 1
        if goal_actor in paths:
            print(paths[goal_actor])
            return paths[goal_actor]
        else:
            return None

    return None
        
        
    
    

def bacon_path(transformed_data, actor_id):
    # start is bacon, start for other functions will be that specific actor
    
    paths_to_actor = find_path(transformed_data, actor_id)
    return paths_to_actor


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    return find_path(transformed_data, actor_id_2, actor_id_1)

def movie_path(transformed_data, path):
    movies = []
    for i in range(len(path) - 1):
        movies.append(transformed_data[path[i]][path[i+1]])
    return movies

def actor_path(transformed_data, actor_id_1, goal_test_function):
    return find_path(transformed_data, start_id=actor_id_1, goal_test_function=goal_test_function)


def actors_connecting_films(transformed_data, film1, film2):
    actor_id_1 = None
    actor_id_2 = None
    
    for actor in transformed_data: 
        if actor_id_1 and actor_id_2:
            break
               
        values = set(transformed_data[actor].values())
        if film1 in values and actor_id_1 == None:
            actor_id_1 = actor
        if film2 in values and actor_id_2 == None:
            actor_id_2 = actor
    
    return actor_to_actor_path(transformed_data, actor_id_1, actor_id_2)


if __name__ == "__main__":
    with open("Lab 3/bacon/resources/large.pickle", "rb") as f:
        f2 = open("Lab 3/bacon/resources/names.pickle", "rb")
        f3 = open("Lab 3/bacon/resources/movies.pickle", "rb")
        db = pickle.load(f)
        # print(db)
        # print(actors_with_bacon_number(transform_data(db), 6))
        # print(pickle.load(f2)["Robert Viharo"]) # SH: 572600, RV: 109625
        # f2.close()
        namesdb = pickle.load(f2)
        moviesdb = pickle.load(f3)
        path = actor_to_actor_path(transform_data(db),namesdb["Dan Fogelman"], namesdb["Vjeran Tin Turk"])
        movie_path = movie_path(transform_data(db), path)
        # # print(namesdb['Brendan Mee'])
        # to_names = {1367972, 1345461, 1345462, 1338716}
        # print([name for name, id in namesdb.items() if id in to_names])
        names_list = []
        for movieid in movie_path:
            names_list.extend([name for name, id in moviesdb.items() if id == movieid])
        print(names_list)
        # print([name for name, id in namesdb.items() if id in path])
        f2.close()
        f3.close()

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
