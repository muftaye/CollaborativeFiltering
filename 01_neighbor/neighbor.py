#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 02:01:52 2018

@author: james.f.xue
"""

#%%
import numpy as np
import math 
import pandas as pd
import random

processed_directory = "../data/processed"
output_directory = "../data/output"

#%%
class Similarity: 
        
    def inner_product(self, u, v): 
        return np.dot(u, v)
    
    def cosine_similarity(self, u, v): 
        return (np.dot(u, v))/(math.sqrt(np.dot(u, u))*math.sqrt(np.dot(v, v)))
    
    def pearson_similarity(self, u, v): 
        #make this for nonzero only
        mean_u = np.mean(u)
        mean_v = np.mean(v)
        
        u_centered = u-mean_u 
        v_centered = v-mean_v 
        top = (np.dot(u_centered, v_centered))
        bot = (math.sqrt(np.dot(u_centered, u_centered))*math.sqrt(np.dot(v_centered, v_centered)))
        if bot == 0: 
            result = 0 
        else: 
            result = top/bot
        
        return result
        
    """TODO FIX""" 
    def user_based(self, dataframe, *metric): 
        (Y, X) = matrix.shape 
        result_matrix = np.empty((Y, Y))
        #for each row in matrix, iterate through all the rows
        
        for i, row_i in enumerate(matrix): 
            for j, row_j in enumerate(matrix): 
                if metric == "cosine": 
                    score = self.cosine_similarity(row_i, row_j)
                else: 
                    score = self.pearson_similarity(row_i, row_j)
                result_matrix[i, j] = score 
                
        return result_matrix 

#%%
sim= Similarity() 
sim.pearson_similarity([0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 0, 0, 0, 0])

#%%
class NeighborPredict(): 
    
    def purchase_predict(self, onehot_data, output_directory, k_neighbors): 
        df = pd.read_csv(onehot_data, ",").drop(['Unnamed: 0'], axis=1) 
        df_columns = df.columns
#        print(df_columns) 
        onehot_array = np.array(df)
        users = onehot_array[:, 0]
        onehot_games = onehot_array[:, 1:]
        sim = Similarity()
        
        """Create Similarity Matrix""" 
        similarity_matrix = np.empty((len(users), len(users)))
        
        """TODO Rerun this""" 
        """Begin Toggler""" 
#        for i, row1 in enumerate(onehot_games): 
#            for j, row2 in enumerate(onehot_games): 
#                if (i!=j): 
#                    similarity_matrix[i][j] = sim.cosine_similarity(row1, row2)
#                else: 
#                    similarity_matrix[i][j] = 0 
#        
#        temp = pd.DataFrame(similarity_matrix)
#        temp.to_csv(output_directory+"/similarity_matrix_purchase.csv")
        """End Toggler""" 
        
        temp = pd.read_csv(output_directory+"/similarity_matrix_purchase.csv", ",").drop(['Unnamed: 0'], axis=1)
        similarity_matrix = np.array(temp)
        
        for i, row in enumerate(onehot_games): 
            """Change for Time Case, nonzero Average doesn't mean much here since it's all 1""" 
            user_average = np.mean(row) #don't use here
            for j, purchase in enumerate(row):
                if purchase == 0: 
                    similarity_array = similarity_matrix[i]
                    mask = (onehot_games[:, j] > 0)
                    masked_similarity = similarity_array[mask]
                    top_k_indices = masked_similarity.argsort()[-k_neighbors:][::-1]
                    
                    """We run into the problem where the number of neighbors is less than k"""
                    top = 0
                    bottom = 0 
                    for index in top_k_indices: 
                        if masked_similarity[index] != 0 : 
                            print(masked_similarity[index])
                            top += masked_similarity[index] 
                            bottom += 1
                    
                    if bottom == 0 : 
                        onehot_games[i][j] == 0
                    elif (top/bottom > 0): #change to 0.5
                        onehot_games[i][j] == 1
                        print("found")

        
#        result = np.concatenate((nonehot_games), axis=1)      
        result = pd.DataFrame(onehot_games, columns = df_columns[1:]) #set column names
        result.to_csv(output_directory+"/predicted_onehot_purchase_random.csv")
        
        return result.shape 
    
    def playtime_predict(self, onehot_data, similarity_name, output_name, k_neighbors): 
        df = pd.read_csv(onehot_data, ",").drop(['Unnamed: 0'], axis=1) 
        df_columns = df.columns
#        print(len(df_columns))
#        print(df_columns) 
        onehot_array = np.array(df)
        users = onehot_array[:, 0]
        onehot_games = onehot_array[:, 1:]
        sim = Similarity()
        
        """Create Similarity Matrix""" 
        similarity_matrix = np.empty((len(users), len(users)))
        
        """TODO Rerun this""" 
        """Begin Toggler""" 
        for i, row1 in enumerate(onehot_games): 
            for j, row2 in enumerate(onehot_games): 
                if (i!=j): 
                    similarity_matrix[i][j] = sim.pearson_similarity(row1, row2)
                else: 
                    similarity_matrix[i][j] = 0 
        
        temp = pd.DataFrame(similarity_matrix)
        temp.to_csv(similarity_name)
        print("similarity_matrix")
        """End Toggler""" 
        
        temp = pd.read_csv(similarity_name, ",").drop(['Unnamed: 0'], axis=1)
        similarity_matrix = np.array(temp)
        
        nonzero_average_matrix = []
        for row in onehot_games: 
            if np.count_nonzero(row) != 0:     
                average = sum(row)/np.count_nonzero(row)
                nonzero_average_matrix.append(average)
            else: 
                nonzero_average_matrix.append(0)
        
        for i, row in enumerate(onehot_games): 
            """Change for Time Case, nonzero Average doesn't mean much here since it's all 1""" 
            for j, purchase in enumerate(row):
                if purchase == 0: 
                    similarity_array = similarity_matrix[i]
                    mask = (onehot_games[:, j] > 0)
                    masked_similarity = similarity_array[mask]
                    top_k_indices = masked_similarity.argsort()[-k_neighbors:][::-1]
                    
                    """We run into the problem where the number of neighbors is less than k"""
                    top = 0
                    bottom = 0 
                    for index in top_k_indices: 
                        if masked_similarity[index] != 0 :
                            top += masked_similarity[index] * (onehot_games[index][j] - nonzero_average_matrix[index])
                            bottom += abs(masked_similarity[index])
                    
                    if bottom == 0 : 
                        onehot_games[i][j] == 0
                    else: #change to 0.5
#                        print(bottom)
                        onehot_games[i][j] ==  top/bottom
                    

        
#        result = np.concatenate((nonehot_games), axis=1)   
        users = pd.DataFrame(users)
        onehot_games = pd.DataFrame(onehot_games)
#        print(onehot_games.shape)
        result = pd.concat([users, onehot_games], axis=1)
#        print(result.shape)
        result.columns = df_columns
        result.to_csv(output_name)
        
        return result 

        



#%%
purchase_random = processed_directory+"/one_hot_random.csv"
purchase_top = processed_directory+"/one_hot_top.csv"
playtime_random = processed_directory+"/one_hot_playtime_random.csv"
playtime_top = processed_directory+"/one_hot_playtime_top.csv"

purchase_random_predict = output_directory+"/one_hot_random_predict.csv"
purchase_top_predict = output_directory+"/one_hot_top_predict.csv"
playtime_random_predict = output_directory+"/one_hot_playtime_random_predict.csv"
playtime_top_predict = output_directory+"/one_hot_playtime_top_predict.csv"

playtime_similarity_top_predict = output_directory+"/similarity_playtime_top_predict.csv"
playtime_similarity_random_predict = output_directory+"/similarity_playtime_random_predict.csv"

#%%
neighbor = NeighborPredict() 
neighbor.playtime_predict(playtime_random, playtime_similarity_random_predict, playtime_top_predict, 5)
#purchase = neighbor.playtime_predict(loc, filename, 10)



#%%

class Evaluation: 
    
    def cross_validate(self, tidy_df, onehot_df, train=0.7, val=0.15, test= 0.15): 
        row_length = tidy_df.shape[0]
        train_length = int(row_length * train)
        val_length = int(row_length * val)
        indices = list(range(0, row_length))
#        print(indices)
        
        train_indices = random.sample((indices), train_length)
#        print(len(train_indices))
        train_split = tidy_df.iloc[train_indices]
        
        new_indices = []
        for i in indices: 
            if i not in train_indices: 
                new_indices.append(i)
#        print(new_indices)
        val_indices = random.sample((new_indices), val_length)
        val_split = tidy_df.iloc[val_indices]
        
        newest_indices = []
        for i in new_indices: 
            if i not in val_indices: 
                newest_indices.append(i)
        
#        print(newest_indices)
        test_split = tidy_df.iloc[newest_indices]
        
        """Remove Val Split and Test Split from Onehot df"""
        withhold_split = pd.concat([val_split, test_split])
        withhold_np = np.array(withhold_split)
        for row in withhold_np: 
#            print("row", row)
            user = row[0]
            game = row[1]
            onehot_df.loc[onehot_df.user_id == user, game] = 0
        
        onehot_df.to_csv(processed_directory+"/one_hot_playtime_crossvalidated.csv")
        print("saved")

        return train_split, val_split, test_split, onehot_df
        
    
    def accuracy(self, prediction_matrix, val, test): 
        
        """Giving the outlier prone nature of our data, MAE is a good fit"""
        """RMSE is also ok""" 
        val_MAE = 0 
        val_RMSE = 0 
        test_MAE = 0 
        test_RMSE = 0
        
        val_split = np.array(val)
        test_split = np.array(test)
        
        for row in val_split: 
            user = row[0]
            game = row[1]
            time = row[2]
            
            prediction = prediction_matrix.at[prediction_matrix.user_id == user, game] 
            
            abs_diff = abs(time-prediction)
            sq_diff = abs_diff ** 2 
            val_MAE += abs_diff
            val_RMSE += sq_diff
            
        val_len = val_split.shape[1]
        val_MAE = val_MAE / val_len
        val_RMSE = math.sqrt(val_RMSE / val_len)
        
        
        for row in test_split: 
            user = row[0]
            game = row[1]
            time = row[2]
#            print(user, game, time)
            

            prediction = prediction_matrix.at[prediction_matrix.user_id == user, game] 
            prediction = prediction[0]
            print(prediction)
            print("-"*10)
            
            abs_diff = abs(time-prediction)
            sq_diff = abs_diff ** 2 
            test_MAE += abs_diff
            test_RMSE += sq_diff
            
        test_len = test_split.shape[1]
        test_MAE = test_MAE / test_len
        test_RMSE = math.sqrt(test_RMSE / test_len)
        
        print(val_MAE, val_RMSE, test_MAE, test_RMSE)
        
        return val_MAE, val_RMSE, test_MAE, test_RMSE


#%%
ev = Evaluation()
tidy1 = pd.read_csv(processed_directory+"/play_tidy_random.csv", ",").drop(['Unnamed: 0'], axis=1)
onehot1 = pd.read_csv(processed_directory+"/one_hot_playtime_random.csv", ",").drop(['Unnamed: 0'], axis=1)
train, val, test, onehot_df = ev.cross_validate(tidy1, onehot1)
#%%
#playtime_random_cv = pd.read_csv(processed_directory+"/one_hot_playtime_crossvalidated.csv").drop(['Unnamed: 0'], axis=1)
playtime_random_cv = processed_directory+"/one_hot_playtime_crossvalidated.csv"
temp_result = neighbor.playtime_predict(playtime_random_cv, playtime_similarity_random_predict, playtime_random_predict, 5)

#%%

#%%
val1, val2, test1, test2 = ev.accuracy(temp_result, val, test)
#%%
print(val1, val2, test1, test2)


#%%
print(val1)



#%%