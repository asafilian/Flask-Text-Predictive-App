# Flask Text Predictive App
SAF Predictive Text is a web-based application suggesting words the end user may wish to insert in a text field.  
The R Shiny app version of this prorduct can be found at https://asafilian.shinyapps.io/as_txtpredict/, and its corresponding repository at https://github.com/asafilian/Predictive_Text_Shiny_App. 

I analyzed a large corpus of text documents (more than 4 million lines, and over 102 million words) to discover the relationship between words. 
The primary training data for this project was provided by Swiftkey.
 
This app is based on an n-gram model (unigrams to hexa-grams) to predict next words given a phrase. 
I followed the Stupid Backoff method in building the models. 
To calculate the n-gram probabilities, I used the Kneser-Ney smoothing method. 
The final data is stored in AWS RDS (MySQL). 

This repository includes the following folders:
1. **pred-text-prep**
	- Contains Python files you need to preprocess, build a model for the product. The final data (ngrams probabilities) are pickled.
	- Run the files in the following order:
		1. `corpus_info_split.py`
		2. `preprocess_text.py`
		3. `ngrams.py`
		4. `modeling.py`
		5. `clean_optimize_probs.py`
	- The final DataFrames are stored as pickled objects. These can can found in the folder **data_pickled** in the repository.
2. **db-create**
	- Used to create a MySQL database. You should put your connections in the DATABASE_URI variable. The given DataFrames can be found in the folder **data_pickled**.
3. ***flask-pretictivetext***
	- The FLASK application including the prediction of next words.


***The running web-based product can be found at:***

http://saf-predictivetext.us-east-2.elasticbeanstalk.com/ 