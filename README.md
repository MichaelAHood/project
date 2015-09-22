# Personalized Real Estate Recommender
This is the real estate recommendation system that I built for my final project during the Galvanize Data Science Intesive.

In short, the recommender is designed to help a person who is moving from one city to another, find a place to live. 
This is accomplished by serving two listings at the same time and allowing the user to choose the one they like the best.

The results are recorded and used to learn the users preference for certain types of homes. 

The recommendations are served based on a pair-wise similarity matrix that is computed using multiple custom distance metrics. Each distance metric corresponds to a preference for a certain type of house, e.g. spaciousness, walkability, etc. 

To determine the actual preference for a user, an implementation of the Bayesian Multi-Armed Bandit (MAB) apporach to AB testing is used. As data is collected about a users preferences, the results are used to update the algorithms best guess about what type of user you are (i.e. what are your preferences for a home). The algorithm is biased to serve recommendations in accordance with the best guess, as will also serve recommendations from other similarity metrics -- chosen at random.

This repo is a work in progress and is continually updated as I make progress on my project.

# Documentation

## 1. Data Pipeline
  a. Web scraping
  b. API's

## 2. Cleaning and Processing
  a. Dealing with missing values
  b. 
## 3. Implementing the Recommender

