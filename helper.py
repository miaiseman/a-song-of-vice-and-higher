#-------------------------------------
# Library Dependencies
#------------------------------------
import numpy as np
from itertools import chain

#-------------------------------------
# Functions
#------------------------------------

def get_keys(path):
    """
    Given a path to json file, returns the keys

    Parameters
    ---------
    path: path with file name of json file

    Returns
    -------
    returns: dict of keys
    """
    import json 
    
    with open(path) as f:
        return json.load(f)

def attribute_comment(df, map_dict):
    """Put character's name in the character's column if it mentioned in the comment."""
    for index, row in df.iterrows(): #loop thru comments
        for key, value in map_dict.items(): #loop through dictionary
            df.loc[index,key]= int(0)
            for item in value:
                if item in row['comment']:
                    df.loc[index, key] += int(row['comment'].count(item))
                    
def add_comment_length_column(df):
    """Add the length of the comment to our dataframe (which has a column named 'comment'.)"""
    for index, row in pol_df.iterrows():
        pol_df.loc[index,'comment_length']= len(pol_df['comment'][index])
    return

def create_person_mat(tgt_persons, person_dict):
    """
    Given dictionary of persons to their search terms,
    create matrix that returns location of matches (denoted by 1).
    The dictionary is screened using a list of target persons

    Parameters
    ---------
    tgt_person_dict: dictionary, where key indicates person, and value is a list
    of potential search terms

    Returns
    -------
    returns: nxm numpy matrix, where n in the # of persons in tgt_person_dict
    and m is the number of total search terms
    """
    
    # Create new tgt_person_dict, based on target persons
    tgt_person_dict = {}
    for person in tgt_persons:
        if person in person_dict.keys():
            tgt_person_dict[person] = person_dict[person]
    
    # Create list of all search terms
    terms = list(chain(*tgt_person_dict.values()))

    # Create starter zero matrix 
    person_mat = np.zeros((len(tgt_person_dict), len(terms)))
    
    # Create dict of person indices -> row ids
    person_ids = {}
    for idx, name in enumerate(tgt_person_dict.keys()):
        person_ids[name] = idx
  
    # Create dict of term indices -> column ids
    term_ids = {}
    for idx, term in enumerate(terms):
        term_ids[term] = idx        
 
    # Fill person_mat with ones using the indices above
    for name, terms in tgt_person_dict.items():
        person_id = person_ids[name]
        for term in terms:
            term_id = term_ids[term]
            person_mat[person_id, term_id] = 1 
            
    return person_mat

def create_scores_matrix(topn, similars_dict, vocab):
    """
    Create a matrix of similarity scores, given dictionary of results

    Parameters:
    ----------
    topn: number of similar words requested
    similars_dict: dictionary version of the most.similar's list of tuples
    
    Returns:
    --------
    scores_mat: returns a matrix of scores of dimension:
                topn x length of vocab
    """
    # Make list of just similar words
    similar_words = [key_val for key_val in similars_dict]     
    
    # Create zeroes matrix
    scores_mat = np.zeros((topn, len(vocab)))

    # Loop throught the vocab
    for i, search_term in enumerate(vocab):
        col = i
        # If person in similar words list, retrieve the score
        if search_term in similar_words:
            row = similar_words.index(search_term) 
            score = similars_dict[search_term]
            scores_mat[row, col] = score

    return scores_mat    
    
def add_similarity_score(tgt_word, topn, w2v_model
                         , tgt_df, term_vocab, person_mat):
    """Given a target word, run through prefit gensim Word2Vec model and
        retrieve topn most similar words. And then append average score
        to person dataframe.

    Parameters:
    ----------
    tgt_word: term to search for most similarity
    topn: number of similar words requested
    w2v_model: pre-trained gensim Word2Vec model
    tgt_df: dataframe to column-bind average results
    term_vocab: Get vocab list of search terms used to search for persons
    person_mat: mapping matrix to map person to respective search terms

    Returns:
    --------
    Nothing. Just prints completion message.
    """

    # Get most similar words
    similars = w2v_model.wv.most_similar(tgt_word, topn=topn)

    # Store as dict
    similars_dict = { term[0]: term[1] for term in similars}
    
    # Create scores matrix
    scores_mat = create_scores_matrix(topn, similars_dict, term_vocab)
    scores_matched_mat = (scores_mat @ person_mat).T

    # Get vector of summed similarity scores
    agg_similarity = np.sum(scores_matched_mat, axis=1) 
    
    # Get vector of count of term matches 
    match_count = np.count_nonzero(scores_matched_mat, axis=1)
    
    # Get average similarity for tgt word to person
    with np.errstate(divide='ignore', invalid='ignore'):
        avg_similarity = np.nan_to_num(np.divide(agg_similarity, match_count))
    
    # Append onto target dataframe
    tgt_df['similarity_' + tgt_word] = avg_similarity

    print("Completed for :'" + tgt_word + "'")
    
#-------------------------------------
# Dictionaries
#------------------------------------
    
### Mapping for person to search terms
person_dict = {'bran':['bran','brandon stark'], 
            'jon':['jon', 'jon snow'], 
            'dany':['khaleesi', 'dany', 'daenerys', 'danyris','danny','danaerys', 'daenarys'], 
           'davos':['davos'],
            'doran':['doran'],
            'cersei':['cersei','cercei'],
            'tyrion':['tyrion', 'tirion'],
            'sansa':['sansa'],
            'arya':['arya'],
            'stannis':['stannis'],
            'varys':['varys','varis'],
            'jamie':['jamie','jaime'],
            'brienne':['brienne', 'brianne'],
            'samwell':['samwell'],
            'jorah':['jorah'],
            'theon':['theon'],
            'hound':['hound', 'sandor'],
            'littlefinger':['littlefinger', 'baelish'],
            'joffrey':['joffrey','joff'],
            'mountain':['mountain', 'gregor'],
            'robb':['robb'],
            'dragons':['drogo', ],
            'melisandre':['melisandre'],
            'bronn':['bronn'],
            'gilly':['gilly'],
            'ramsey':['ramsey', 'ramsay'],
            'missandei':['missandei'],
            'gendry':['gendry'],
            'grey worm':['grey worm', 'greyworm', 'gray worm', 'grayworm'],
            'ned':['ned', 'eddard'],
            'catelyn':['catelyn'],
            'tormund':['torumund','tormund', 'giantsbane'], #fixed 190614
            'robert':['robert'],
            'tommen':['tommen'],
            'viserys':['viserys'],
            'margaery':['margaery'],
            'euron':['euron'],
            'oberyn':['oberon', 'oberyn', 'viper', 'red viper'],
            'night_king':['night king', 'nightking', ' nk '],'lyanna':['lyanna mormont'],
            'jaqen':['jaqen'], 'hodor':['hodor'], 'ygritte':['ygritte'], 'mance':['mance'],
               'harris':['senator harris', 'k. harris', 'kamala', 'kamalaharrisforpresident'], 
             'biden':['biden', 'joe2020'],
             'buttigieg':['buttigieg', 'buttigidg', 'mayor pete', 'bootijedge'], 
             'gillibrand':['gillibrand', 'kirsten'], 'hickenlooper':['hickenlooper'], 
             'klobuchar':['klobuchar'], 'warren':['warren','elizabeth'], 
             'booker':['booker','cory'], 'inslee':['inslee'], 
             'castro':['castro', 'julián', 'julian'], 'gabbard':['gabbard', 'tulsi'], 
             'sanders':['sanders', 'bernie', 'feelthebern'], 'de blasio':['de blasio','deblasio','blasio'], 
             'bullock':['bullock'], 'gravel':['gravel'], 
             'messam':['messam'], "o'rourke":["o'rourke", "beto"], 
             'bennet':['bennet'], 'delaney':['delaney'], 
             'moulton':['moulton'], 'swalwell':['swalwell'], 
             'williamson':['williamson'], 'yang':['yang']}
        

# Mapping for person to domain
domain_dict = {'bran': 'got'
                ,'jon': 'got'
                ,'dany': 'got'
                ,'davos': 'got'
                ,'doran': 'got'
                ,'cersei': 'got'
                ,'tyrion': 'got'
                ,'sansa': 'got'
                ,'arya': 'got'
                ,'stannis': 'got'
                ,'varys': 'got'
                ,'jamie': 'got'
                ,'brienne': 'got'
                ,'samwell': 'got'
                ,'jorah': 'got'
                ,'theon': 'got'
                ,'hound': 'got'
                ,'littlefinger': 'got'
                ,'joffrey': 'got'
                ,'mountain': 'got'
                ,'robb': 'got'
                ,'dragons': 'got'
                ,'melisandre': 'got'
                ,'bronn': 'got'
                ,'gilly': 'got'
                ,'ramsey': 'got'
                ,'missandei': 'got'
                ,'gendry': 'got'
                ,'grey worm': 'got'
                ,'ned': 'got'
                ,'catelyn': 'got'
                ,'tormund': 'got'
                ,'robert': 'got'
                ,'tommen': 'got'
                ,'viserys': 'got'
                ,'margaery': 'got'
                ,'euron': 'got'
                ,'oberyn': 'got'
                ,'night_king': 'got'
                ,'lyanna': 'got'
                ,'jaqen': 'got'
                ,'hodor': 'got'
                ,'ygritte': 'got'
                ,'mance': 'got'
                ,'harris': 'dems'
                ,'biden': 'dems'
                ,'buttigieg': 'dems'
                ,'gillibrand': 'dems'
                ,'hickenlooper': 'dems'
                ,'klobuchar': 'dems'
                ,'warren': 'dems'
                ,'booker': 'dems'
                ,'inslee': 'dems'
                ,'castro': 'dems'
                ,'gabbard': 'dems'
                ,'sanders': 'dems'
                ,'de blasio': 'dems'
                ,'bullock': 'dems'
                ,'gravel': 'dems'
                ,'messam': 'dems'
                ,"o'rourke": 'dems'
                ,'bennet': 'dems'
                ,'delaney': 'dems'
                ,'moulton': 'dems'
                ,'swalwell': 'dems'
                ,'williamson': 'dems'
                ,'yang': 'dems'
              }     

