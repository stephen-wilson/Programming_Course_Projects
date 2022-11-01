# Recipes Database
# NO ADDITIONAL IMPORTS!
from distutils.dep_util import newer, newer_pairwise
import sys
from venv import create

sys.setrecursionlimit(20_000)


def replace_item(recipes, old_name, new_name):
    """
    Returns a new recipes list based on the input list, where all mentions of
    the food item given by old_name are replaced with new_name.
    
    If tuple[0] is compound, check tuple[1] and the corresponding tuple[0] of each tuple in the
    corresponding ingredient list.
    If tuple[0] is atomic, check tuple[1]. Add to new list of tuples but replace old_name with new_name.
    
    
    """
    recipes = recipes.copy()
    new_recipes = []
    for recipe in recipes:
        if recipe[0] == "atomic": 
            if recipe[1] == old_name:
                new_recipes.append(("atomic", new_name, recipe[2]))
            else:
                new_recipes.append(recipe)
        elif recipe[0] == "compound":
            if recipe[1] == old_name:
                new_recipes.append(("compound", new_name, recipe[2]))
            else:
                subrecipes_to_add = recipe[2].copy() # copy subrecipes list
                for i in range(len(subrecipes_to_add)):
                    if subrecipes_to_add[i][0] == old_name:
                        subrecipes_to_add[i] = (new_name, subrecipes_to_add[i][1])
                new_recipes.append(("compound", recipe[1], subrecipes_to_add))
                
    return new_recipes
                        
# CREATE THE REPRESENTATION
def create_recipe_dict(recipes, to_ignore):
    ignore_food = set(to_ignore)
    recipes_dict = {}
    for recipe in recipes:
        if recipe[1] not in ignore_food:
            if recipe[0] == "compound":
                if recipe[1] not in recipes_dict:
                    recipes_dict[recipe[1]] = [recipe[2]]
                else:
                    recipes_dict[recipe[1]].append(recipe[2])
            elif recipe[0] == 'atomic':
                recipes_dict[recipe[1]] = recipe[2]
                
    return recipes_dict

def sum_values(dictionaries):
    new_dict = {}
    for _dict in dictionaries:
        for key in _dict.keys():
            if key not in new_dict:
                new_dict[key] = _dict[key]
            else:
                new_dict[key] += _dict[key]
                
    return new_dict

def lowest_cost(recipes, food_item, to_ignore=[]):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    
    Represent the data just as a list of length 2 tuples, name and then tuple[1] is list if compound.
    recurse into list of length 2 tuples jusrt as if it had been the original list, etc.
    ABOVE, NO!!
    
    *ACTUAL*: have a dictionary representation:
    keys are names of recipes, values is just the price if atomic, list of ingredients if compound
    
    example:
    {'cookie sandwhich': [[('cookie', 2), ('ice cream scoop', 2), ...], []],
    'cookie': [[(sugar, 2)...], [(chocolate chip, 2)]],
    'sugar': 5,
    'ice cream scoop': ..., 
    ...}
    """
    ### Creating the representation
    recipes_dict = create_recipe_dict(recipes, to_ignore)
    ####
    
    # Recursive function
    def find_lowest_cost(food):
        """
        Algorithm: Find food item in dict. If value is list, loop through each value (another list)
        and then recurse through each of those ingredients. Each outer list is its own possible sum
        
        If value is a list, loop through each ingredient in the list and 
        
        Base case: if food is instance int, return that value.
        """
        if food in recipes_dict:
            # base case
            if isinstance(recipes_dict[food], (int, float)):
                return recipes_dict[food]
            # recursive case
            else:
                # part 6.0 solution
                # return min((sum(item[1] * find_lowest_cost(item[0]) for item in recipe_list)) 
                #            for recipe_list in recipes_dict[food] )
                # part 6.1 solution
                sums = []
                for recipe_list in recipes_dict[food]:
                    to_sum = []
                    for item in recipe_list:
                        if item[0] in recipes_dict:
                            lowest_cost = find_lowest_cost(item[0])
                            if lowest_cost:
                                to_sum.append(item[1]*lowest_cost)
                        else:
                            break

                    if len(to_sum) == len(recipe_list):
                        sums.append(sum(to_sum)) 
                
                return min(sums) if sums else None                       
                ####
            
        return None
    
    return find_lowest_cost(food_item)
        
def scale_recipes(amount, atomic_ingredients):
    """
    Scales amount of ingredient by the amount of the given item
    
    Ex:
    cookie: (sugar, 3), (milk, 4)
    milk: (milking stool, 1), (cow, 2)
    {cow: 1 * 2 * 4} {milking stool: 1 * 4} {sugar: 1 * 3}
    
    Do step by step:
    cookie: (sugar, 3), (milk, 4)
    {cow: 1 * 2 * 4} {milking stool: 1 * 4}
    """
    # if atomic_ingredients:
    #     if type(atomic_ingredients) is not list:
    #         scaled_ingredients = {}
    #         for key, value in atomic_ingredients.items():
    #             scaled_ingredients[key] = value * amount
    #         return scaled_ingredients
    #     else:
    #         scaled_list = []
    #         for ingredients in atomic_ingredients:
    #             scaled_ingredients = {}
    #             for key, value in ingredients.items():
    #                 scaled_ingredients[key] = value * amount
    #             scaled_list.append(scaled_ingredients)
    #         return scaled_list
    # else:
    #     return None
    
    if atomic_ingredients:
        assert type(atomic_ingredients) != list
        scaled_ingredients = {}
        for key, value in atomic_ingredients.items():
            scaled_ingredients[key] = value * amount
        return scaled_ingredients
    else:
        return None
    
def find_cheapest_cost(recipes_dict, ingredients_list):
    current_min = [float('inf'), None]
    for ingredients in ingredients_list:
        sum = 0
        for ingredient in ingredients.keys():
            sum += recipes_dict[ingredient] * ingredients[ingredient]
        if sum < current_min[0] and ingredients:
            current_min[0], current_min[1] = sum, ingredients
    return current_min[1]
        

def cheapest_flat_recipe(recipes, food_item, to_ignore=[]):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing a full recipe for
    the given food item.
    
    Algorithm: Want to find the lowest costing recipe and return the atomic ingredients of that recipe.
    Recurse down an ingredient list until finding atomic elements. Add them to a dictionary with the
    keys mapping to the ingredient name, and the values being the amount. Then lookup in another dictionary to 
    find the cost of the atomic ingredients, multiply by the amount, and sum the costs, all using a helper
    function. Return the dictionary that returns the lowest amount.
    
    Return format:
    {'atomic food': amount, 'atomic food 2': amount2}
    """
    recipes_dict = create_recipe_dict(recipes, to_ignore)
    
    def find_cheapest_flat_recipe(food):
        list_of_recipes = []
        if food in recipes_dict:
            # base case
            if isinstance(recipes_dict[food], (int, float)):
                return {food: 1}
            # recursive case
            else:
                for recipes_list in recipes_dict[food]:
                    recipes = {}
                    for item in recipes_list:
                        scaled_recipe = scale_recipes(item[1], find_cheapest_flat_recipe(item[0]))
                        if not scaled_recipe:
                            recipes = {}
                            break
                        else:
                            for k,v in scaled_recipe.items():
                                if k in recipes:
                                    recipes[k] += v
                                else:
                                    recipes[k] = v
                    list_of_recipes.append(recipes)
                # loop over and return cheapest
                return find_cheapest_cost(recipes_dict, list_of_recipes)
        else:
            return None
        
    
                    
    
    # # recursive function
    # def find_cheapest_flat_recipe(food):
    #     if food in recipes_dict:
    #         # base case
    #         if isinstance(recipes_dict[food], (int, float)):
    #             return food
    #         # recursive case
    #         else:
    #             pass
                
                
    # # def cheapest_recipe(recipes):
    # #     return recipes[0]
                
        
            
    # return  find_cheapest_flat_recipe(food_item)

    # # ATTEMPT 2
    # def find_cheapest_flat_recipe(food):
    #     # base case
    #     if isinstance(recipes_dict[food], (int, float)):
    #         return {food: 1}
    #     # recursive case
    #     else:
    #         # part 6.0 solution
    #         # return min((sum(item[1] * find_lowest_cost(item[0]) for item in recipe_list)) 
    #         #            for recipe_list in recipes_dict[food] )
    #         # part 6.1 solution
    #         # cheap_recipe = {}
    #         # return cheap_recipe | find_cheapest_flat_recipe(food)
            
            
    #         sums = []
    #         for recipe_list in recipes_dict[food]:
    #             to_sum = []
    #             for item in recipe_list:
    #                 if item[0] in recipes_dict:
    #                     cheap_recipe = find_cheapest_flat_recipe(item[0])
    #                     print(item[1])
    #                     if lowest_cost:
    #                         to_sum.append({cheap_recipe: item[1]})
    #                 else:
    #                     break

    #             if len(to_sum) == len(recipe_list):
    #                 sums.extend(to_sum) 
            
    #         return {key: value for recipe_dict in sums for key, value in recipe_dict.items() } if sums else None

    return find_cheapest_flat_recipe(food_item)

def all_flat_recipes(recipes, food_item, to_ignore=[]):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.
    """
    recipes_dict = create_recipe_dict(recipes, to_ignore)
    # print(f'cheese: {recipes_dict["cheese"]}')
    
    # need to somehow NOT add a recipe list to the dictionary if one of the recursed elements returns None
    
    def find_all_recipes(food):
        list_of_recipes = []
        if food in recipes_dict:
            print(recipes_dict[food])
            # base case - if atomic
            if isinstance(recipes_dict[food], (int, float)):
                return [{food: 1}]
            # recursive case - if compound
            else:
                # for each food_item in recipes_dict[food], for each of food item's possible recipes,
                # scale the recipes by the amount of that food item needed by food
                for recipe_list in recipes_dict[food]:
                    recipes = {}
                    print(f'rl: {recipe_list}')
                    for item in recipe_list:
                        scaled_recipes = []
                        # if item[0] in recipes_dict and None not in recipes:
                        if item[0] in recipes_dict:
                            for recipe in find_all_recipes(item[0]):
                                print(f'recipe: {recipe}')
                                if recipe:
                                    scaled_recipes.append(scale_recipes(item[1], recipe))
                                # else:
                                #     print(recipe, item)
                                #     scaled_recipes = []
                                #     break
                                # list_of_recipes.append(scale_recipes(item[1], recipe))
                            print(scaled_recipes)
                            # CREATE HELPER FUNCTION FOR COMBINING THE CURRENT LIST OF DICTIONARIES,
                            # WITH THE LIST OF DICTIONARIES FOR THE SUBPROBLEM OF THE OTHER WAYS TO MAKE
                            # THE FOOD
                            for scaled in scaled_recipes:
                                    for k,v in scaled.items():
                                        if k in recipes:
                                            recipes[k] += v
                                        else:
                                            recipes[k] = v
                        else:
                            # recipes = {None: None}
                            recipes = {}
                            break
                    if recipes:
                        list_of_recipes.append(recipes)
                    # if len(recipes) >= len(recipe_list):
                    # if None in recipes:
                    #     list_of_recipes.append([])
                    # if None not in recipes:
                    #     list_of_recipes.append(recipes)
                return list_of_recipes
        else:
            return []
        
        
        
        list_of_recipes = []
        if food in recipes_dict:
            # base case
            if isinstance(recipes_dict[food], (int, float)):
                return [{food: 1}]
            # recursive case
            else:
                for recipes_list in recipes_dict[food]:
                    recipes = {}
                    for item in recipes_list:
                        # recipes = {}
                        all_recipes = find_all_recipes(item[0])
                        scaled_recipes = []
                        # scale_recipe = {}
                        for recipe in all_recipes:
                            # scale the recipe
                            scale_recipe = scale_recipes(item[1], recipe)
                            if not scale_recipe:
                                scaled_recipes = []
                                break
                            else:
                                scaled_recipes.append(scale_recipe)
                        print(len(scaled_recipes), len(all_recipes), scaled_recipes, all_recipes)
                        if len(scaled_recipes) != len(all_recipes):
                            recipes = {}
                            break
                        # update the recipes dictionary with the scale
                        else:
                            for scaled in scaled_recipes:
                                for k,v in scaled.items():
                                    if k in recipes:
                                        recipes[k] += v
                                    else:
                                        recipes[k] = v
                    if recipes:
                        list_of_recipes.append(recipes)
                # return the recipes
                return list_of_recipes
        else:
            return []
    
    
    
    return find_all_recipes(food_item)
    
    # return NotImplementedError
    recipes_dict = create_recipe_dict(recipes, to_ignore)
    
    flat_recipes = []
    
    def find_flat_recipe(food):
        # base case
        if isinstance(recipes_dict[food], (int, float)):
            return food
        # recursive case
        else:
            for recipe_list in recipes_dict[food]:
                flat_recipe = {}
                for item in recipe_list:
                    return {find_flat_recipe(item[0]): item[1]}
                    
                    flat_recipe | {find_flat_recipe(item[0]): item[1]}
                # flat_recipes.append(flat_recipe)
                #     flat_recipes.append({find_flat_recipe(item[0]): item[1]})
            
    
    # if food_item in recipes_dict:
    #     for recipe_list in recipes_dict[food_item]:
    #         flat_recipe = find_flat_recipe(food_item)
    #         # find_flat_recipe() should return None if an ingredient does not exist
    #         if flat_recipe: flat_recipes.append(flat_recipe)
    find_flat_recipe(food_item)        
    print(flat_recipes)
    return flat_recipes

if __name__ == "__main__":
    # you are free to add additional testing code here!
    smaller_recipes = [
    ('compound', 'chili', [('cheese', 2), ('protein', 3), ('tomato', 2)]),
    ('compound', 'milk', [('cow', 1), ('milking stool', 1)]),
    ('compound', 'cheese', [('milk', 1), ('time', 1)]),
    ('compound', 'protein', [('cow', 1)]),
    ('atomic', 'cow', 100),
    ('atomic', 'tomato', 10),
    ('atomic', 'milking stool', 5),
    ('atomic', 'time', 10000),
    ]
    print(replace_item(smaller_recipes, 'milk', 'chocolate milk'))
    
    """
    Result:
    [('compound', 'chili', [('cheese', 2), ('protein', 3), ('tomato', 2)]), 
    ('compound', 'chocolate milk', [('cow', 1), ('milking stool', 1)]), 
    ('compound', 'cheese', [('chocolate milk', 1), ('time', 1)]), 
    ('compound', 'protein', [('cow', 1)]), 
    ('atomic', 'cow', 100), 
    ('atomic', 'tomato', 10), 
    ('atomic', 'milking stool', 5), 
    ('atomic', 'time', 10000)]  
    
    [
    ('compound', 'chili', [('cheese', 2), ('protein', 3), ('tomato', 2)]),
    ('compound', 'chocolate milk', [('cow', 1), ('milking stool', 1)]),
    ('compound', 'cheese', [('chocolate milk', 1), ('time', 1)]),
    ('compound', 'protein', [('cow', 1)]),
    ('atomic', 'cow', 100),
    ('atomic', 'tomato', 10),
    ('atomic', 'milking stool', 5),
    ('atomic', 'time', 10000),
]
    """
