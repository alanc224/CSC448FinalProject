# CSC448 Final Project
# Music Recommendation Model
Descripton here, Maybe include slides here

We are creating an interactive music recommendation model which is capable of taking in a song name given by a user, and then outputting a song or list of songs that that has similar characteristics based on numerical data which can represent said characteristics from our datasets. 

The current restrictions we face in terms of functionality is that the model will only work if the inputted song also has an entry in the datasets we use, as that way we will have its characteristics labeled numerically, which we can then compare to other songs in the dataset to detect similarities. One way we can potentially help rectify this is by implementing a model which can detect similarity between text, so that if a user inputs a song name that is not recognized in the dataset, we can query the user to pick from a set of songs that have a similar name to see if they inputted the name incorrectly.

Additionally, we could also potentially use the Spotify API to collect the relavant audio features we need of an inputted song, and using that as input instead of depending on the inputted song already existing in the dataset entries.

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
Need brief description  
[Requirements](requirements.txt) - includes all of the packages used + versions  
[Instructions](instructions.txt) - includes instructions for setting up various parts of the project
# Implementation
Describe how we are implementing models here
# Resources 
Credit any resources here

[Music Dataset : 1950 to 2019 posted by Saurabh Shahane](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019)  
[Spotify dataset posted by Vastal Mavani](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset/data)
