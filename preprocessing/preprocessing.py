#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 02:03:28 2018

@author: james.f.xue
"""

import pandas as pd
import numpy as np
import random

#%%

raw_file_location = "../data/raw/steam-200k.csv"
processed_directory = "../data/processed"
header_names = ['user_id', 'game_name', 'purchase-play', 'indicator-hours', 'empty']
data = pd.read_csv(raw_file_location, names=header_names)

#%%

class preprocessing: 
    """
    Tidying Data
    """
    def tidy(self, data, processed_directory): 
        #subset data into a purchase dataset and a play dataset based on purchase-play
        purchase = data.loc[data['purchase-play'] == 'purchase']
        play = data.loc[data['purchase-play'] == 'play']
    
        """Remove the empty column"""
        play = play[['user_id', 'game_name', 'indicator-hours']]
    
        """Save this file as a csv"""
        play.to_csv(processed_directory+"/play_tidy.csv")
        
        return play
        
    def subsample_random(self, processed_directory): 
        """Read the Data"""
        play_tidy = pd.read_csv(processed_directory+"/play_tidy.csv", ",")
        play_tidy.head()
    
        """sub sample the games to 100 from 3.6k games for a simple model"""
        unique_users = play_tidy['user_id'].unique()
        unique_games = play_tidy['game_name'].unique()
    
        #generate random 100 games
        random_indices = random.sample(range(0, len(unique_games)), 100)
        random_100games = unique_games[random_indices]
    
        #select games from dataframe
        play_tidy_100games = play_tidy.loc[play_tidy['game_name'].isin(random_100games)]
        len(play_tidy_100games['user_id'].unique()) #931 unique users
        play_tidy_100games = play_tidy_100games.drop(['Unnamed: 0'], axis=1)
    
        #save to csv
        play_tidy_100games.to_csv(processed_directory+"/play_tidy_random.csv")
    
        return play_tidy_100games
    
    def subsample_top(self, processed_directory): 
        #returns games purchased by over 100 users
        """Read the Data"""
        play_tidy = pd.read_csv(processed_directory+"/play_tidy.csv", ",")
        play_tidy = play_tidy.drop(['Unnamed: 0'], axis=1)
    
        """sub sample the games to 100 from 3.6k games for a simple model"""
        unique_users = play_tidy['user_id'].unique()
        unique_games = play_tidy['game_name'].unique()
        
        """Generate Top 100 Games by Purchase Count""" 
        purchase_counts = (play_tidy.set_index(["game_name", 'user_id']).count(level='game_name'))
        purchase_counts = purchase_counts[purchase_counts['indicator-hours'] > 100]
        top_games = purchase_counts.index
        
        top_filter = play_tidy['game_name'].isin(top_games)
        
        play_tidy_top = play_tidy[top_filter]
        play_tidy_top.to_csv(processed_directory+"/play_tidy_top.csv")
        
        return play_tidy_top
            
        
    def one_hot_random(self, processed_directory): 
        """One Hot Encode Results"""
        
        play_tidy_100games = pd.read_csv(processed_directory+"/play_tidy_random.csv", ",")
        play_dummies = pd.get_dummies(play_tidy_100games['game_name'])
        one_hot_random = pd.concat([play_tidy_100games['user_id'], play_dummies], axis=1)
        one_hot_random.to_csv(processed_directory+"/one_hot_random.csv")
        
        return one_hot_random
    
    def one_hot_top(self, processed_directory): 
        """One Hot Encode Results"""
        
        play_tidy_100games = pd.read_csv(processed_directory+"/play_tidy_top.csv", ",")
        play_dummies = pd.get_dummies(play_tidy_100games['game_name'])
        one_hot_top = pd.concat([play_tidy_100games['user_id'], play_dummies], axis=1)
        one_hot_top.to_csv(processed_directory+"/one_hot_top.csv")
        
        return one_hot_top
    
    def collapsed_random(self, processed_directory): 
    
        """Collapsed One-Hot by User"""
        one_hot_collapsed = one_hot_100games.groupby(['user_id']).sum()
        one_hot_collapsed.to_csv(processed_directory+"/one_hot_collapsed.csv")
        one_hot_collapsed
        
    
        
    #%%
pre = preprocessing() 
pre.one_hot_top(processed_directory)