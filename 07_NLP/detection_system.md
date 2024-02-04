# Detection Systems

Under the hood, this detection system is a multifunctional NLU system, like spaCy, but based on a monolithic architecture, and with a focus on user-generated content. All the functions are exposed using the same language models and the same analysis process invoked using the POST /parse method. In just one call you're getting entities, sentiment, topic, problematic content, and low-level NLP data. 


## Entity Extraction

These are the types of the entities to extracts:

- person with optional subtypes: 
    - fictional_character (characters from books, movies, etc.), 
    - important person (VIPs, celebrities, historical figures, politicians, etc.), 
    - spiritual being (gods, spirits, etc.)
- organization
- place
- time range
- date
- time
- amount of money
- phone number 
- role - social role (profession, rank, etc.)
- crypto addresses, with optional subtypes: bitcoin, ethereum, monero, monero_payment_id, litecoin, dash
- credit card numbers with subtypes (visa, mastercard, american express, diners club, discovery, jcb, unionpay)
- website
- software
- filename
- ip_address, subtypes: 
    - v4, 
    - v6 (in development)
- mac address
- username

## Language Identification
Detects the language of the utterance. 

## Sentiment Analysis

Sentiment analysis both at the document level and as a breakdown by aspects / facets (so-called "aspect-based sentiment analysis"). 

Note that sentiment analysis and detection of problematic content are not the same. Sentiment can be negative and not be a personal attack or hate speech; on the other hand, criminal activity or sexual advances may not necessarily carry negative sentiment.

