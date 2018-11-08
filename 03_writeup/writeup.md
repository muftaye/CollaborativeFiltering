# NVIDIA Edge: Steam Game Recommendation Engine Report

Muf Tayebaly, Senior Project Lead    
James Xue, Creative Project Manager

### Abstract: Our Business 

At NVIDIA, our course business is to empower gamers across the globe to be able to play their favorite games with the best performance hardware available. We are looking to create NVIDIA Edge, an online server based service for gamers to access the best GPUs in the world remotely and a low cost. The service will include a built-in library of games for Gamers to play at a subscription. We are hoping to determine the library of games to initialize our service with, as well as to recommend players new games as our service and library expands. 

### Objective: What Are We Tackling? 

We are looking to make use of the Steam Video Game dataset to better understand our gamers and determine what we can recommend. 

The Steam gaming platform distributes games to its users and allows for multi-player management and a community for gaming. Game sales is an important revenue stream and some gamers are known to play the same game for long periods of time instead of branching out. With the increasing advertising platforms becoming available (Facebook, Instagram, Snapchat, etc..), costs of advertising can be pricey to gain new sales. Studies have shown (e.g. Waggener Edstrom Worldwide) that word-of-mouth is the primary leader in new game sales.

A recommender system can behave similarly to word-of-mouth where it can help identify new games for a user based on similar users or items. This can lead to more game sales by making the users aware of games they might be interested in without having to pay for expensive advertisements. If the recommendations prove to be successful with the user, it can even increase the validity for the users to continue to use the recommendations going forward to find new games. New sales creates increased revenue and the potential to decrease advertisements costs (if recommendations prove to sell more than advertisements) and therefore increasing profits. While advertisements are good to get the names known to larger audiences, especially those who are unfamiliar with the Steam platform, for existing users, recommendation systems can be very useful and what we will test within this project.

### Objective: Acceptance Criteria

Ultimately, we want to continuously improve as we expand our services and our library of games. However, for the time being, we just want to get a sense of the quality of recommendations we can extract from just user, game, and time played. We would like to see a few suggestions per player since we want targeted, personalized content for our gamers. 

Recommendation systems can even strengthen the gaming community by getting users who are interested in similar games actually playing more of those games together and creating stronger relationships between gamers that can ultimately retain users in the long run.

We will use existing user and game data to prove we can make accurate (to some significance) recommendations of games that we already know the user is interested in since we will hold out known data.

Neighborhood Based Methods

### Overview

We choose to implement a Neighborhood Based Recommendation System by hand due to some customization required by our data. Let’s begin by covering our data and then move on to our methodology and customizations. The data we have consists of several columns: user, game, purchase, and playtime.  The challenge with our data is that it is extremely sparse and the playtime values greatly vary. Out of the tens of thousand games available, most users play less than 10 games. The playtime could vary between several hundred hours played to a few minutes. On another level, we don’t have explicit ratings from the users. We can only implicitly infer their preferences from their hours played. 

These challenges demanded several changes to how we measure performance. 

First of all, due to the sparsity of the matrices, it was impractical and ineffective to remove the mean from the data when calculating predictions. The result of removing the mean is that we have a very, very, very significant number of negative hours played, leading to spurious and nonsensical predictions regarding hours played (many negative hours played predictions). 

Secondly, we choose to create a custom coverage metric based on the catalogue coverage metric. Due to the sparsity of the matrices, many of our similarities between users were actually zero. This resulted in each user being recommended a very small number of games to play (most games had a predicted play time of zero). This means that it might not be effective to look at high ranking items but rather hours played. We set a hyperparameter, minimum hours played and determined the coverage on items that were recommended and predicted to be played over a certain number of hours. For example, for a minimum hour played of 1, we have a coverage metric of 0.14. 

Thirdly, we created custom ways to cross-validate the data. Due to the sparsity of the matrix, it makes no sense to cross validate the one-hot-encoding itself. We cross validate the sample that we have into train, test, and validation. We create the one hot encoding on the entire set but then remove the values associated with test and validation. This cross validated one hot encoding was then used to determine similarity and predictions. 

Fourth, we wanted to have unique sampling methods for the data. Due to the large number of players and games, creating a one hot encoding on the entire set was impractical and slow. Thus, we choose to sample k random games and also k top games to create separate 

Lastly, we wanted to be able to choose our accuracy metric. We wanted to not rely on RMSE since our playtimes have large variations. Furthermore, we belive the MAE could be a good metric as to not overly punish differences from players who played 2000+ hours when compared to the average. Surprisingly, on our random 100 games subsample, we found a validation MAE of 3938.3, validation RMSE of 1452.9, test MAE of 3417.9, and test RMSE of 2186. This shows that most of the differences between predicted and true is less than 1 hours played (since RMSE is the sum of the square difference vs MAE is just the absolute difference). It is also promising that the validation and test are not too different.


### Hyperparameter Effects: Neighborhood Size, Minimum Hours Played, Model Size

Disclaimer: since the methods for the entire neighborhood pipeline is written by me, a good deal of it is not optimized. As a result, there is a limit on the size of the number of games we can consider since anything over 50 games actually takes a while to pipe through the entire preprocessing, one-hot encoding, and prediction phases. Each data point took a significant amount of time to obtain. 

(i) Neighborhood Size: 

This chart shows the difficulty of working with our data. Due to the sparsity of the matrix, the number of neighbors that have nonzero play times for a particular game is inherently very small. Furthermore, these small number of neighbors also tend to be very dissimilar from the user. As a result, changing the size of the neighborhood did not really affect our metrics. On the other hand, this does give a good comparison of the different metrics. MAE tends to be higher than RMSE, indicating small differences in play times on average (less than 1 hour). 



