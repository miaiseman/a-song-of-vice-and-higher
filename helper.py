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