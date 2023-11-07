# CSE 3521
## Spotify Recommender
This repo houses the semester project of:
- Bronson Brown
- Brent Hasseman
- Hifa Mousou

For the Spring 2021 semester of CSE 3521. 
The group has chosen to create a program that takes training data in the form of songs liked or disliked by a user, then uses this data to create a playlist of recommended songs for that same user. The user can then provide feedback on the playlist (and individual songs within it), which the program then uses (through various Machine Learning algorithms) to recommend better songs in the future.

# Library Installation 
If any errors are given due to any libraries not being installed (mainly Spotipy and Pandas), please be sure to use 'pip3 install' to install any necessary libraries.

# Algorithm Testing Instructions
For grading purposes and to show consistency of the program before any extra user input, the test and train csv files with data already entered will be provided. Please be sure to run the ID3 and Naive Bayes files (as instructed below) before running the recommender file to see that the output is consistent from both.

# Instructions for application
Before running the application, ensure that you go to https://accounts.spotify.com/en/login and log in with these credentials: 

Username: testAccount_@gmail.com
Password: ReallyCoolProject123!

After you log in, go to https://developer.spotify.com/dashboard/ and also log in using those same credentials. If you would like to see the playlists getting added to the Spotify account, you can do so using the Spotify desktop application.

To run the recommender, simply select `SpotifyDailyRecommender.py` (in the Recommender folder) as the file to be run and follow the prompts. When selecting the songs from the list it provides as your liked songs, be sure to follow the format "#, #, #, ...". If you do not like any of the songs, simply leave it blank and press enter. Any extra characters, use of numbers outside of the provided list, or other formatting issues will cause the program to fail execution. Once you have completed this, name the playlist anything you want, and follow the prompts again to do it a second time. The first set of prompts you answer will update the data in `train.csv`, and the second set of prompts will update `test.csv`. The created playlists should be reflected in your Spotify application.

To run the ID3 algorithm, `select ID3.py` as the configuration for your compiler to run. There is no input required here - the file will automatically pull the correct csv's needed to create the tree and test against it. It will output specific entropies, info gains, a text version of the tree, predictions, and the overall accuracy. Keep in mind that occasionally due to song attribute similarity and limited attributes/categories, the tree will run out of splits it can make and will inform you that a tree could not successfully be made. In these cases, you will have to create a new training file for the decision tree to make predictions.

To run the Naive Bayes algorithm, first be sure to run the `CsvToDoc.py` file. This will convert the csv files into a bag of words format, which is what the Naive Bayes class will be using to make predictions. Once this is done, select `NBAlg.py` and run it. Again, no input is required here. The file will print predicted sentiments for the songs, as well as its overall accuracy.

