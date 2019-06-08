def get_keys(path):
    """
    Given a path to json file, returns the keys
    Paramters
    ---------
    path: path with file name of json file

    Returns
    -------
    returns: dict of keys
    """
    import json 
    
    with open(path) as f:
        return json.load(f)
     
#cvs file that has two columns - one that is a person and one that is the colloquial reference to that person 
#function that references that list and includes "or" between them? or joins them in some way OR just have the dang list here in this file :) 
#functions that query mondodb? 



