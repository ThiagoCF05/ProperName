# A model for proper name generation

The main model described at Ferreira et al. (2017) is available at [Bayes.py](https://github.com/ThiagoCF05/ProperName/blob/master/main/eacl/models/Bayes.py). 

Here is described in a couple of steps how to work with this model. This example is coded at [bayes_example.py](https://github.com/ThiagoCF05/ProperName/blob/master/main/eacl/models/bayes_example.py)

## Step 1
The model use NLTK as a dependency. Check [the project webpage](http://www.nltk.org/)

## Step 2
Initialize the variable *settings_labels* with all the proper name forms in your dataset. A proper name form consists of 5 elements: 

1. title (+t)
2. first name (+f)
3. middle name (+m)
4. last name (+l)
5. appositive (+a)

## Step 3
Initialize the variable *settings_features* with the discourse features used to describe the references. As explicit in the code, the original model chooses a proper name based on the syntactic position (*syntax*) of the reference and its status in the text (*givenness*) and sentence (*sentence-givenness*).

## Step 4
Initialize the class **Bayes** with the training sets (*train_set_content* and *train_set_realization*) and the variable *bigram*.

### *train_set_content* 
This is the training set for the content selection step of the model. Techinically, this is a list of instances in the following format:

```
		{
	        'entity': 'Barack_Obama',
	        'givenness': 'old',
	        'sentence-givenness': 'new',
	        'syntax': 'np-subj',
	        'label': '+f+l',
	        'label_elems': ['+f', '+l']
    	}
```

1. **entity** id of the mentioned person;
2. **givenness** shows if the entity is text-new ('new') or text-old ('old'); 
3. **sentence-givenness** shows if the entity is sentence-new ('new') or sentence-old ('old');
4. **syntax** syntactic position of the reference (subject - "np-subj"; object - "np-obj" or subject determiner - "subj-det")
5. **label** proper name form of the training instance
6. **label_elems** elements from the proper name form splitted on a list

### *train_set_realization* 
This is the training set for the textual realization step of the model. For the proper name form described in the content selection instance, possible realization instances are:

```
		{
	        'word': 'Barack',
	        'bigram': ('Barack', '*'),
	        'entity': 'Barack_Obama,
	        'givenness': 'old',
	        'sentence-givenness': 'new',
	        'syntax': 'np-subj',
	        'label': '+f+l',
	    },
		{
	        'word': 'Obama',
	        'bigram': ('Obama', 'Barack'),
	        'entity': 'Barack_Obama,
	        'givenness': 'old',
	        'sentence-givenness': 'new',
	        'syntax': 'np-subj',
	        'label': '+f+l',
	    },
	    {
	        'word': 'END',
	        'bigram': ('END', 'Obama'),
	        'entity': 'Barack_Obama,
	        'givenness': 'old',
	        'sentence-givenness': 'new',
	        'syntax': 'np-subj',
	        'label': '+f+l',
	    }
```

It is important to use a start ('*') and end ('END') symbol to guide the model on the test phase. 

### *bigram* 
This variable indicates whether you want to choose a proper noun based on the previous one (True / default option) or not (False).

## Step 5
Once the model is initialized, you can select a proper name form by calling the method *select_content*. The method receives two parameters: *features* and *entity*

### *features*
This variable is a dictionary with the discourse features that describes the reference. Here is one instance for the "Barack Obama" example:

```
		{
            'discourse_se': 'new,
            'sentence_se': 'old,
            'syntax_se': 'np-subj'
        }
```

It is important to observe that the nomenclature changed here. What we called 'givenness' at the training sets is called 'discourse_se' here. The same for 'sentence-givenness'/'sentence_se' and 'syntax_se'/'syntax'. Another thing to be considered is the option to generate a proper name form based only on subset of these features. Let's say that I want to predict a proper name form based only on referntial status of the person in the text. The parameter for method would be:

```
		{
            'discourse_se': 'new,
        }
```

### *entity*

This is the *id* of the person to be referred to. For **Barack Obama** the value would be *Barack_Obama*.

## Step 6

To perform the textual realization step, the function *realize* can be called. It receives 4 parameters:

1. **form** the form of the proper name (according to the values set at settings_labels)
2. **entity** id of the entity
3. **syntax** syntactic position of the reference (*np-subj*, *np-obj*, *subj-det*)
4. **appositive** an string with the appositive to be realized. In case of Barack Obama, this can be *the 44th president of United States*

# Citation


**Creators:** Thiago Castro Ferreira, Emiel Krahmer and Sander Wubben

Tilburg center for Cognition and Communication Department - Tilburg University