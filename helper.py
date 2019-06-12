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
            'ramsey':['ramsey', 'ramsay'],
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
            'oberon':['oberon'],'night_king':['night king'],'lyanna':['lyanna mormont'],
            'jaqen':['jaqen'], 'hodor':['hodor'], 'ygritte':['ygritte'], 'mance':['mance']}

dems_dict = {'harris':['senator harris', 'k. harris', 'kamala', 'kamalaharrisforpresident'], 
             'biden':['biden', 'joe2020'],
             'buttigieg':['buttigieg', 'buttigidg', 'mayor pete', 'bootijedge'], 
             'gillibrand':['gillibrand'], 'hickenlooper':['hickenlooper'], 
             'klobuchar':['klobuchar'], 'warren':['warren'], 
             'booker':['booker'], 'inslee':['inslee'], 
             'castro':['castro', 'julián', 'julian'], 'gabbard':['gabbard', 'tulsi'], 
             'sanders':['sanders', 'bernie', 'feelthebern'], 'de blasio':['de blasio'], 
             'bullock':['bullock'], 'gravel':['gravel'], 
             'messam':['messam'], "o'rourke":["o'rourke", "beto"], 
             'bennet':['bennet'], 'delaney':['delaney'], 
             'moulton':['moulton'], 'swalwell':['swalwell'], 
             'williamson':['williamson'], 'yang':['yang']}
        
def attribute_comment(df, map_dict):
    """Put character's name in the character's column if it mentioned in the comment."""
    for index, row in df.iterrows(): #loop thru comments
        for key, value in map_dict.items(): #loop through dictionary
            df.loc[index,key]= int(0)
            for item in value:
                if item in row['comment']:
                    df.loc[index, key] += int(row['comment'].count(item))
                    
def add_comment_length(df):
    """Add the length of the comment to our dataframe (which has a column named 'comment'.)"""
    for index, row in pol_df.iterrows():
        pol_df.loc[index,'comment_length']= len(pol_df['comment'][index])
                    
                    
     
    




