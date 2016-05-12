# Predicting US Primaries 2016 through Twitter

This project tries to predict the results of the US Primaries 2016 using data from the days preceding each primary. For this, we implement four models - Count, MaxSoFar, BagSentiments and TimeSentiments.

This repo contains a demonstration that can be accessed through the file `demo_nlp.php`

## Requirements for the Project:
* [scikit-learn 0.17.1](http://scikit-learn.org/stable/)
* python-2.7

## Running the models
In order to run the **Count** model:    
`python baseline.py`    
If you want to run the model for a specific place, you can run it through    
`python demo_baseline.py <place>`

In order to run the **MaxSoFar** model:    
`python frequent_permute_data.py`

In order to run the **BagSentiments** model:  
`python new_permute_data.py`

In order to run the **TimeSentiments** model:  
`python permute_data.py`  
If you want to run the model for a specific place, you can run it through  
`python demo_predict.py <place> <number of days to Primary>`

## Approach
A paper describing the approach has been added to this folder itself by the name of `Predicting Elections through Twitter.pdf`
