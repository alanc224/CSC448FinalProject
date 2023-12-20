# CSC448 Final Project
# Music Recommendation Model

We are creating an interactive music recommendation model that is capable of taking in a song (in the form of a Spotify URL) given by a user, and then outputting a list of songs that have similar characteristics based on the numerical data that represents said characteristics from our datasets. The user has the option to choose from 4 different unsupervised machine learning recommendation models (created from 2 distinct models and 4 different dimensionality reduction). More information can be found in the implementation section.

We also implemented the Spotify API that allows us to process the input song and extract its audio attributes and features of the song to compare it to the characteristics of the songs from our dataset. Additionally, we also use the Spotify API to provide audio samples below (if available) the outputted list of song recommendations, so that users can access the song more efficiently to judge if they like it or not.

<p align="center">
    <details>
        <summary>Presentation Slides</summary>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/1.jpg"/>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/2.jpg"/>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/3.jpg"/>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/4.jpg"/>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/5.jpg"/>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/6.jpg"/>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/7.jpg"/>
        <img src="https://github.com/alanc224/CSC448FinalProject/blob/main/Documents/Presentation_Images/8.jpg"/>
    </details>
</p>

# Group 4 (TBD)
[Alan Concepcion](./Code/Alan_Concepcion/) - Created and structued the gitub; created a K-NN model with factor analysis for the back-end; assisted in front-end development; set up the keys for the Spotify API; structured the report.   

[Konrad Zielinski](./Code/Konrad_Zielinski/) - Created a K-NN model which uses feature agglomeration to perform dimensionality reduction; created the basis for the front-end functionality; created the basis for our flask backend and connected it to the front-end; wrote for the Modeling and K-Nearest Neighbors sections, as well as the FeatureAgglomeration section in the report.  

[Anthony Zhu](./Code/Anthony_Zhu/) - Created a K-Means Clustering model with feature selection to group the data songs in the data set into 10 clusters and integrated the model with the flask app.  

[Daphne Tang](./Code/Daphne_Tang/) - Created a K-means model with low variance filtering for the back-end; integrated the model into the flask application; created visualizations for the Analysis part; proofread and edited the report; wrote the K-means Clustering and Low Variance Filter sections in the report.  
# Installaton
[Requirements](requirements.txt) - includes all of the packages used + versions  
install all neccessary packages using requirements.txt

     - Creating a virtual environment may be preferred before this step.
     Documentation on how to create a virtual environment - (https://docs.python.org/3/library/venv.html)
    1. run the following command: "pip install -r requirements.txt"
        

Set up and use environment variables from .env file

    1. create a new file in VScode, name it ".env"
    2. declare variables in the .env file as you would in any other python file
        - The environment variable 'SPOTIFY_DATA' should be the path for the Spotify Dataset after extracting to your desired location.
            Example: Within .env the environment variable may look like [ SPOTIFY_DATA = path/to/the/spotify/data/set/here ] 
    3. import load_dotenv from dotenv package in whatever file you want to use the .env variable
    4. type "load_dotenv()" into your file and then get the variable you need using "os.getenv("VARIABLE_NAME_HERE)"

Running the application

    1. In order to run the application, make sure the aforementioned steps have been completed. 
        - Installation of all the necessary packages
        - cd into the Code directory
        - Run the command flask run
            - This will run the python file app.py
    
# Implementation
Libraries used in our Project:
 * **Pandas**;  used for reading the datasets, creating one of our own, and exploratory data analysis
 * **dotenv /os**; used to create environmental variables
 * **Spotipy**; Spotify API that allows us to show audio previews and album art covers in our application and helps us process the user input and retrieve information to use in our models
 * **Sklearn**; using k-means and k-nearest neighbors unsupervised learning models rather than implementing the two from scratch, using the scalers from the preprocessing library, using normalize to normalize the variable values for low variance filter
 * **Matplotlib**; this is used to create graphs for analysis purposes
 * **Factor_analyzer**; this is used for the factor analysis portion of this report
 * **Seaborn**; used for some visualizations
 * **Plotly.express**; used to create most of the data visualizations
   
Our flask application gives the user the option to choose between 4 distinct unsupervised machine learning models: K-Nearest Neighbors, K-Means Clustering, K-NN with FAR, and K-Means with LVF. <br>
The models used in our project are K-means clustering and K-nearest neighbors. We decided on 2 unsupervised learning models while using 4 distinct dimension reduction techniques.  The reduction techniques used are Factor Analysis,  FeatureAgglomeration Reduction, Feature Selection reduction, and Low Variance Filter. 

# Resources 
[Spotify dataset posted by Vastal Mavani](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset/data)
