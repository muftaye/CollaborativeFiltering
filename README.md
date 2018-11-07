# Personalization Project

Phase 1: 
-> Preprocessing (Current)

comment 1: 
- I have made a tidy version of the data, just need to transform it into sparse. 
- The project actually doesn't need so many users and games, so we can limit the number of users and games before transforming into sparse. 

- Taking a random sample is giving a very empty matrix.  I think we need to filter for like top users and top games for hours played and then take a random sample.

Phase 2: 
Modeling
Evaluation

Phase 3: 
Write Up/Business Case
Clean up Github Repo.


# Personalization Project - Part 1 HW2
**Team:**  Muf Tayebaly (mt3195), James Xue (jx2181)  
**Data Set:**  Steam Video Game (Kaggle)

### Objective
The Steam gaming platform distributes games to its users and allows for multi-player management and a community for gaming.  Game sales is an important revenue stream and some gamers are known to play the same game for long periods of time instead of branching out.  With the increasing advertising platforms becoming available (Facebook, Instagram, Snapchat, etc..), costs of advertising can be pricey to gain new sales.  Studies have shown (e.g. Waggener Edstrom Worldwide) that word-of-mouth is the primary leader in new game sales. 

A recommender system can behave similarly to word-of-mouth where it can help identify new games for a user based on similar users or items.  This can lead to more game sales by making the users aware of games they might be interested in without having to pay for expensive advertisements.  If the recommendations prove to be successful with the user, it can even increase the validity for the users to continue to use the recommendations going forward to find new games.  New sales creates increased revenue and the potential to decrease advertisements costs (if recommendations prove to sell more than advertisements) and therefore increasing profits.  While advertisements are good to get the names known to larger audiences, especially those who are unfamiliar with the Steam platform, for existing users, recommendation systems can be very useful and what we will test within this project.

Recommendation systems can even strengthen the gaming community by getting users who are interested in similar games actually playing more of those games together and creating stronger relationships between gamers that can ultimately retain users in the long run.

We will use existing user and game data to prove we can make accurate (to some significance) recommendations of games that we already know the user is interested in since we will hold out known data.

## Model-based - Matrix Factorization
### Data Preprocessing
The Steam data was provided as a CSV with rows containing details of user-game purchased and hours played values.  We preprocessed the data by creating 3 separate files: customers.csv (contains a list of unique customers and a new indexed ID), games.csv (contains a list of game names and a new unique game ID), and hours.csv (contains list of hours played for each customer and game using the new IDs). We used new IDs to help speed up processing and keep a good sense of customers and games.

### Sampling Data
For part 1, we decided to keep to a smaller data set as described in the instructions to gain better intuition on the data, testing and exploring.  Since there was a lot of games that users did not really play and have data for, we decided to start with popular games so we filtered to games that were played by more than 50 users which gave 284 games.  Out of those games we randomly sampled 90 games to use.

Now that we had the games, we wanted to ensure we had the right users since there are a lot of users who would not have played any of those 90 games and therefore would not provide good recommendations with zero rows/columns.  In order to work around this, we filtered the hours played list to only show the user-game hours played for the games in scope (from sample).  This gives us a list of only customers who played our sampled games.  To prevent hold-out issues between train and test data from holding out all of a customers hours played rating, we further filtered the customers unique list by those customers who had played more than 1 game.  This decreases the likelihood of randomly holding out the rating for customer-game since that customer had only played that single game we held out.

The sampling also maintains random seeds in case we need to replicate a run and can also specify new random seeds to get entirely new random data for cross-validations.

### Train and Test Data
Using our sampled data of popular random games, customers who played more than 1 of the games sampled and the ratings list (customer-game hours played), we derived what our train and test data was by holding out data from the ratings (hours played) list.  For example, one run we held out 10% of data for test and the remaining was used for training.  We could then use the train data to create the sparse matrix and have the test data to measure accuracy.

### Matrix Factorization

