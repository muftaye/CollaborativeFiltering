# Personalization Project

Phase 1: 
-> Preprocessing (Current)

comment 1: 
- I have made a tidy version of the data, just need to transform it into sparse. **Update** I have made a sparse set with whether the user has bought the game. 
- The project actually doesn't need so many users and games, so we can limit the number of users and games before transforming into sparse. **Update** I selected 100 random games to geneerate the sparse matrix. 

Phase 2: 
Modeling
- Begun work on Neighbhorhood based model

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
We used the Implicit package as recommended in the project instructions so we could get a feel for how the data was being factored into latent spaces, our data is implicit, and the package runs quickly.  Using the Alternating Least Squares method, we fit the model on the sparse matrix and got the U (customers) and V (games) factored matrices.  The multiplication of these matrices gives us the estimated (learned) matrix R. 

We tried using the squared error to measure accuracy from the estimated matrix R as compared to the test data we held out, but it looked like due to the large range of hours played (which we treated as a rating for the customer-game) the gap between the recommended and actual is high and thus gives a high squared error.

Another accuracy method which we thought worked better for this specific model was to compare the top 10 recommendations and if the test game actually played by the customer was one of the top 10 recommended games.  This gave a good idea of whether or not the model was properly recommended the games to the users and we started seeing roughly 40-50% accurate recommendations.

### Parameter Testing
We used the latent factor spaces as one of our parameters to see how it impacted the accuracy measure.  Using the top 10 recommendation comparison measure, we were able to see a very small factor space was not as good as a medium size (2 factors as compared to 6 factors).  As we went increased the factor spaces, we hit a maximum and then started seeing a decline in accuracy as the factors got too large.  See the figure below which shows you which number of latent factor spaces worked better as compared to others.

### Going Forward
We should be able to use what we learned here to better expand on our models and recommendation techniques for the final project.  We have implicit data of games purchased which can be brought into the picture and also help where we had large range in ratings (hours played) which could have impacted the recommendations.  We did not use any side information which might help as well if we tried to pull some information on these games which can also help determine right factored spaces.  Potentially creating our own Matrix Factorization algorithm for this particular dataset may also prove to work better given certain tweaks.  Lastly, reviewing how the sample we used here as compared to other methods of sampling could show us something we did not notice.
