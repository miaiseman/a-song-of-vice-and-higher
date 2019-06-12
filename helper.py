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
     
got_dict = {'bran':['bran','brandon stark'], 
            'jon':['jon', 'jon snow'], 
            'dany':['khaleesi', 'dany', 'daenerys', 'danyris'], 
           'davos':['davos'],
            'doran':['doran'],
            'cersei':['cersei'],
            'tyrion':['tyrion'],
            'sansa':['sansa'],
            'arya':['arya'],
            'stannis':['stannis'],
            'varys':['varys'],
            'jamie':['jamie'],
            'brienne':['brienne'],
            'samwell':['samwell'],
            'jorah':['jorah'],
            'theon':['theon'],
            'hound':['hound', 'sandor'],
            'littlefinger':['littlefinger', 'baelish'],
            'joffrey':['joffrey'],
            'mountain':['mountain', 'gregor'],
            'robb':['robb'],
            'dragons':['drogo', ],
            'melisandre':['melisandre'],
            'bronn':['bronn'],
            'gilly':['gilly'],
            'ramsey':['ramsey'],
            'missandei':['missandei'],
            'gendry':['gendry'],
            'grey worm':['grey worm'],
            'ned':['ned', 'eddard'],
            'catelyn':['catelyn'],
            'torumund':['torumund'],
            'robert':['robert'],
            'tommen':['tommen'],
            'viserys':['viserys'],
            'margaery':['margaery'],
           }
   
dems_dict = {'harris':['senator harris', 'k. harris', 'kamala'], 'biden':['biden'],
             'buttigieg':['buttigieg', 'buttigidg', 'mayor pete', 'bootijedge'], '':[''], 
             'gillibrand':['gillibrand'], 'hickenlooper':['hickenlooper'], 
             'klobuchar':['klobuchar'], 'warren':['warren'], 
             'booker':['booker'], 'inslee':['inslee'], 
             'castro':['castro'], 'gabbard':['gabbard'], 
             'sanders':['sanders'], 'de blasio':['de blasio'], 
             'bullock':['bullock'], 'gravel':['gravel'], 
             'messam':['messam'], "o'rourke":["o'rourke"], 
             'bennet':['bennet'], 'delaney':['delaney'], 
             'moulton':['moulton'], 'swalwell':['swalwell'], 
             'williamson':['williamson'], 'yang':['yang']}
             

def attribute_comment(comment):
    """Put character's name in the character column."""
    #look at comment 
    #if comment contains a name from the dictionary, put it in the column 
    




