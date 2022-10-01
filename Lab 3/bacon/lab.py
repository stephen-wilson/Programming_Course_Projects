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
            transformed_data[actor1]["actors"].add(actor2)
        else:
            transformed_data[actor1] = {"movie": film, "actors": {actor2}}
        if actor2 in transformed_data:
            transformed_data[actor2]["actors"].add(actor1)
        else:
            transformed_data[actor2] = {"movie": film, "actors": {actor1}}
    
    # return {(actor1, actor2): film for (actor1, actor2, film) in raw_data}
    return transformed_data


def acted_together(transformed_data, actor_id_1, actor_id_2):
    # if actor_id_1 == actor_id_2 and not (actor_id_1, actor_id_2) in transformed_data:
    #     for key in transformed_data.keys():
    #         print("inside for loop!")
    #         print(key)
    #         if key[0] == actor_id_1:
    #             return True
    #         elif key[1] == actor_id_1:
    #             return True
    #     return False
    # return ((actor_id_1, actor_id_2) in transformed_data or 
    #         (actor_id_2, actor_id_1) in transformed_data)
    
    if actor_id_1 == actor_id_2:
       return actor_id_1 in transformed_data 
   
    return actor_id_1 in transformed_data and actor_id_2 in transformed_data[actor_id_1]['actors']
    
    
    
    
# global variable
# paths = {}
def actors_with_bacon_number(transformed_data, n):
    """
    Given the transformed data (graph), calculates the actors
    which have the shortest path of length n to Mr. Bacon.
    
    Returns:
    actors_with_bacon_num (set): actor IDs with bacon number as described above
    """
    baconID = 4724
    
    acted_with_bacon = transformed_data[baconID]['actors']
    bacon_num_actors = [acted_with_bacon]
    visited = acted_with_bacon.copy()
    visited.add(baconID)
    # paths = {actor: [4724, actor] for actor in acted_with_bacon}
    # for actor in acted_with_bacon:
    #     paths[actor] = [4724, actor]
    
    if acted_with_bacon and n > 0:
        if n == 1:
            return acted_with_bacon
        i = 1
        while i < n and bacon_num_actors[i-1]:
            actors_to_add = set()
            for prev_actor in bacon_num_actors[i-1]:
                # get all the actors on this level (bacon num level)
                temp_actors = set()
                # path_to_current = [4724]
                for actor in transformed_data[prev_actor]['actors']:
                    if actor not in visited:
                        temp_actors.add(actor)
                        visited.add(actor)
                        # keep track of the paths to each actor from bacon levels
                        # if prev_actor in paths:
                        #     # print(f"prev: {prev_actor}")
                        #     # print(paths)
                        #     print(prev_actor, paths[prev_actor], type(paths[prev_actor]))
                        #     temp_copy = paths[prev_actor].copy()
                        #     temp_copy.append(actor)
                        #     paths[actor] = temp_copy # is .copy() needed?
                        # else:
                        #     paths[actor] = [4724, actor]
                actors_to_add = actors_to_add.union(temp_actors)
                
            bacon_num_actors.append(actors_to_add)
            i += 1
        if not bacon_num_actors[i-1]:
            return set()
    else:
        return {baconID}
    
    return bacon_num_actors[n-1]

# def find_path(transformed_data, source_node, goal_node, visited, path):
    
#     path.append(source_node)
#     # visited[i] == True
#     visited.add(source_node)
#     if source_node == goal_node:
#         return path
#     for actor in transformed_data[source_node]['actors']:
#         if actor not in visited:
#             return find_path(transformed_data, actor, goal_node, visited, path)
    
#     path.pop() 
#     return None

def find_path(transformed_data, goal_actor, start_id=4724):
    if goal_actor == start_id:
        return [start_id]
    
    paths = {}
    
    acted_with_start_actor = transformed_data[start_id]['actors']
    bacon_num_actors = [acted_with_start_actor]
    visited = acted_with_start_actor.copy()
    visited.add(start_id)
    # paths = {actor: [4724, actor] for actor in acted_with_bacon}
    for actor in acted_with_start_actor:
        paths[actor] = [start_id, actor]
    
    current_actor = start_id
    if acted_with_start_actor:       
        i = 1 
        while goal_actor not in paths and bacon_num_actors[i-1]:
            # actors_to_add = set()
            for prev_actor in bacon_num_actors[i-1]:
                # get all the actors on this level (bacon num level)
                # temp_actors = set()
                if len(bacon_num_actors) <= i:
                    bacon_num_actors.append(set())
                # path_to_current = [4724]
                for actor in transformed_data[prev_actor]['actors']:
                    if actor not in visited:
                        bacon_num_actors[i].add(actor)
                        visited.add(actor)
                        # keep track of the paths to each actor from bacon levels
                        if prev_actor in paths:
                            # print(f"prev: {prev_actor}")
                            # print(paths)
                            # print(prev_actor, paths[prev_actor], type(paths[prev_actor]))
                            temp_copy = paths[prev_actor].copy()
                            temp_copy.append(actor)
                            paths[actor] = temp_copy # is .copy() needed?
                        # else:
                        #     paths[actor] = [4724, actor]
                # actors_to_add = actors_to_add.union(temp_actors)
                
            # bacon_num_actors.append(actors_to_add)
            i += 1
        if goal_actor in paths:
            return paths[goal_actor]
        else:
            return None
        # if not bacon_num_actors[i-1]:
        #     return set()
    # else:
    #     # return {baconID}

    return None
    # return bacon_num_actors[n-1]
    
# # USING BFS
# def FIND_PATH(transformed_data, goal_node, start_node=4724):
#     visited = set()
#     # stack = []
#     path = {}
#     # keep keys in insertion order to implement the queue (FIFO)
#     queue = {}
    
#     # current node is last element in queue
#     # check current node, if not goal node, add childern to queue
#     # pop current node
#     # iterate until queue is empty
    
#     # maybe use double linked list?
#     # keep track of previous node and how many times went forward, that way can delete that many times
#     # in linked list to return back to a chaining that contains a set for looking up nodes on same "level"
    
#     # stack.append(start_node)
#     queue[start_node] = None
#     current_node = start_node
#     prev_node = None
    
#     paths = [[start_node]]
    
#     if start_node == goal_node:
#         return [start_node]
    
#     while queue != {}:
#         # pop only the first element in O(1) for Queue implementation of a sequence interface
#         # i.e. dequeue(x) = delete_first(x)
#         current_node = queue.pop(next(iter(queue)))
#         visited.add(current_node)
        
#         # check current node:
#         if current_node == goal_node:
#             # return path to that node
#             # begin backtracking
#             return path[current_node]
        
#         # if not == to goal node, add its children to stack
#         if current_node in transformed_data and transformed_data[current_node]['actors'] != set():
#             for actor in transformed_data[current_node]['actors']:
#                 if actor not in visited:
#                     # note: queue(x) = insert_last(x)
#                     queue[actor] = None
        
        
#         # if prev_node == None:
#         #     path[current_node] = [current_node]
#         # else:
#         #     temp_copy = path[prev_node].copy()
#         #     temp_copy.append(current_node)
#         #     path[current_node] = temp_copy
            
        
    
    
    
        
        
#         prev_node = current_node
        
#     return path[goal_node]
        
        
    
    

def bacon_path(transformed_data, actor_id):
    # start is bacon, start for other functions will be that specific actor
    # visited = [False]*
    # visited = set()
    # path = []
    # start_node = 4724
    # goal_node = actor_id
    # # adjActors = transformed_data[start_node]['actors']
    
    # if actor_id == 4724:
    #     return [4724]
    # return find_path(transformed_data, start_node, goal_node, visited, path)
        
    # generate paths in global environment using the actors_with_bacon_number function
    # actors_with_bacon_number(transformed_data, n=6)
    paths_to_actor = find_path(transformed_data, actor_id)
    # if actor_id not in paths_to_actor:
    #     return None
    # elif actor_id == 4724:
    #     return []
    return paths_to_actor
    
    
    
    
    # # while we haven't reached the end of a path
    # while adjActors:
    #     for actor in adjActors:
    #         current_node = actor
    #         if current_node == goal_node:
    #             path.append(current_node)
    #             return path
    #         else:
    #             while 
            
    #         visited.add(current_node)
        
    # raise NotImplementedError("Implement me!")


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    return find_path(transformed_data, actor_id_2, actor_id_1)


def actor_path(transformed_data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == "__main__":
    with open("Lab 3/bacon/resources/large.pickle", "rb") as f:
        f2 = open("Lab 3/bacon/resources/names.pickle", "rb")
        db = pickle.load(f)
        # print(db)
        # print(actors_with_bacon_number(transform_data(db), 6))
        # print(pickle.load(f2)["Robert Viharo"]) # SH: 572600, RV: 109625
        # f2.close()
        namesdb = pickle.load(f2)
        path = actor_to_actor_path(transform_data(db),namesdb["Wilbur Mack"], namesdb["Gabriel Jarret"])
        # # print(namesdb['Brendan Mee'])
        # to_names = {1367972, 1345461, 1345462, 1338716}
        # print([name for name, id in namesdb.items() if id in to_names])
        names_list = []
        for actorid in path:
            names_list.extend([name for name, id in namesdb.items() if id == actorid])
        print(names_list)
        # print([name for name, id in namesdb.items() if id in path])
        f2.close()

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
