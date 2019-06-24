# Libraries
import os             # file system stuff
import json           # digest json
import praw           # reddit API
import pandas as pd   # Dataframes
import pymongo        # MongoDB
import numpy as np    # math and arrays

import time           # To time stuff

import helper     # Custom helper functions

#Data storage
from sqlalchemy import create_engine # SQL helper
import psycopg2 as psql #PostgreSQL DBs


#############################################################
def get_subs_df(praw_reddit
                ,subreddit_nm='all'
                ,query=''
                ,results_lim=1000
               ):
    """
    Query a subreddit and return a dataframe of submissions
    Parameters:
    -----------
    praw_reddit: pre-instantiated praw Reddit class
    subreddit_nm: name of subreddit to search
    query: query string to search on
    results_lim: number of submissions results to return
    
    
    Returns:
    --------
    Pandas dataframe of submissions
    """

    # Instantiate subreddit
    subred = praw_reddit.subreddit(subreddit_nm) 
    

    # Get Search generator
    search_results = subred.search(query, 
                            sort='comments',
                           limit=results_lim
                           ,time_filter='month')


    # Compile submission into list
    title = [] 
    num_comments = []
    upvote_ratio = []
    sub_id = []
    i=0

    # Loop through generator and get data
    for submission in search_results:
        i+=1
        title.append(submission.title)
        num_comments.append(submission.num_comments)
        upvote_ratio.append(submission.upvote_ratio)
        sub_id.append(submission.id)
        if i%100 == 0:
            print(f'{i} submissions completed')

    # Make dataframe to hold results        
    df_subs = pd.DataFrame(
        {'title': title,
         'num_comments': num_comments,
         'upvote_ratio': upvote_ratio,
         'id':sub_id
        })

    return df_subs

#############################################################
def get_comms_df(praw_reddit, list_sub_ids=[]):
    """
    Query a list of submission id's get the comments for each submission
    and store in dataframe
    Parameters:
    -----------
    praw_reddit: pre-instantiated praw Reddit class
    list_sub_ids: list of submission ids
    
    Returns:
    --------
    Pandas dataframe of comments
    """    
    # List to hold all the comments dfs
    comm_dfs = []

    # Loop through list sub ids and get comments data
    for this_sub_id in list_sub_ids:
        subm = praw_reddit.submission(id=this_sub_id)
        
        # Instantiate lists to hold comments data
        comment_body = []
        comment_id = []
        sub_id = []

        # Force loading comments until maxed out
        while True:
            try:
                subm.comments.replace_more()
                break
            except PossibleExceptions:
                print('Handling replace_more exception')
                sleep(1)

        # Loop through comments and put into list
        
        for comment in subm.comments.list():
            comment_id.append(comment.id)
            comment_body.append(comment.body)
            sub_id.append(this_sub_id)
            
        # create df from lists
        this_df = pd.DataFrame({
            'comment': comment_body,
            'comment_id':comment_id,
            'sub_id':sub_id
        })

        # Add this sub's comments df to list of dfs
        comm_dfs.append(this_df)
        
    # Combine the list of dataframes
    df_combined = pd.concat(comm_dfs, axis=0).reset_index(drop=True)

    return df_combined
   
#############################################################
def get_subred_subs_coms(praw_reddit
                         ,sql_alch_engine 
                         ,subreddit_nm='all'
                         ,query=''
                         ,results_lim=1000
                         ,nm_subs_tbl='tbl_subs'
                         ,nm_comms_tbl='tbl_comms'
                         ):
    """
    Given the name of a subreddit and search terms, get submissions and their 
    related comments and save them to an AWS DB
    Parameters
    ---------
    praw_reddit: pre-instantiated praw Reddit class
    subreddit_nm: name of subreddit to search
    query: query string to search on
    results_lim: number of submissions results to return
    nm_subs_tbl: name of the submissions table
    nm_comms_tbl: name of the comments table
    sql_alc_engine: SQLAlchemy engine, for pandas to connect 

    Returns
    -------
    No return object, but will print success
    """

    # Start timing
    start_time = time.time()
    now = time.ctime(int(time.time()))
    print('Starting: ' + str(now) + '\n')
    
    
    print('Searching on these terms:\n\n' + query + '\n\n')
    
    # Get Submissions dataframe
    subs_df = get_subs_df(praw_reddit=praw_reddit
                          ,subreddit_nm=subreddit_nm
                          ,query=query
                          ,results_lim=results_lim)
    
    print("Retrieved submissions.\n\n")
    
    # Get just submissions IDs
    list_sub_ids = subs_df['id'].tolist()
    
    # Get comments dataframe
    comms_df = get_comms_df(praw_reddit=praw_reddit
                            ,list_sub_ids=list_sub_ids)
    
    
    print("Retrieved comments.")

    # Write dataframes out to SQL DB
    print('Writing to ' + nm_subs_tbl + '\n\n')
    subs_df.to_sql(nm_subs_tbl, con=sql_alch_engine, if_exists='append')

    print('Writing to ' + nm_comms_tbl + '\n\n')
    comms_df.to_sql(nm_comms_tbl, con=sql_alch_engine, if_exists='append')

    # Timing Stuff
    end_time = time.time()
    now = time.ctime(int(time.time()))
    print('\nFinished: ' + str(now)  + '\n\n')

    mins_to_complete = (end_time - start_time)/60 
    print("It took {:.2f} minutes to complete.\n\n".format(mins_to_complete))
    print("There were {} submissions added.\n\n".format(subs_df.shape[0]))
    print("There were {:,} comments added.\n\n".format(comms_df.shape[0]))
    
    return