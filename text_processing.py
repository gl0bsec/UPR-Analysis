#%%
# File conversion functions
from countryinfo import CountryInfo
import pycountry 
import pandas as pd 
# import spacy
import re

#%%
# Used to generate the Datasets 

def is_valid_country(country_name):
    try:
        country_info = CountryInfo(country_name)
        return country_info.info() is not None
    except:
        return False

def extract_country_treaty(target,text,treaties):
    treaty_abv = treaties['Treaty']
    substrings = treaties['Query']
    results = []
    
    # List to hold the extracted data
    data = []

    # Splitting the text into sentences based on semicolons
    sentences = text.split(";")

    # Defining the regular expression pattern to extract treaties and countries
    pattern = re.compile(r'(.*?)(\((.*?)\))+')

    # Iterating through each sentence to extract treaties and countries
    for sentence in sentences:
        matches = pattern.findall(sentence)
        if matches:
            treaty = matches[0][0].strip()
            for match in matches:
                country = match[2]
                if country and is_valid_country(country):
                    data.append((country, treaty))
                    
    
    for substring in substrings:
        for d in data:
            if substring.lower() in d[1].lower():
                results.append((target,d[0],treaty_abv[substrings.tolist().index(substring)],substring,d[1]))
            # else:
            #     results.append((target,d[0],"NOT FOUND","NOT FOUND",d[1]))
                

    # Creating a DataFrame with the extracted data
    df = pd.DataFrame(results, columns=['Target Country','Source Country', 'Treaty','Full Name','Mention'])
    return df

def count_countries(text):
    # Preprocess the text to remove special characters and split into words
    words = re.findall(r'\b\w+\b', text)

    # Initialize a dictionary to store the country name counts
    country_counts = {}

    # Iterate through the words and check if they match any country names
    for word in words:
        try:
            country = pycountry.countries.get(name=word)
            if country:
                country_name = country.name
                if country_name in country_counts:
                    country_counts[country_name] += 1
                else:
                    country_counts[country_name] = 1
        except LookupError:
            continue
    
    return country_counts


def count_countries_without_regex(text):
    # Split the text into words
    words = text.split()

    # Initialize a dictionary to store the country name counts
    country_counts = {}

    # Iterate through the words and check if they match any country names
    for word in words:
        # Normalize the word by converting to lowercase and removing punctuation
        normalized_word = word.lower().strip(".,!?")

        try:
            country = pycountry.countries.get(name=normalized_word)
            if country:
                country_name = country.name
                if country_name in country_counts:
                    country_counts[country_name] += 1
                else:
                    country_counts[country_name] = 1
        except LookupError:
            continue
    
    return country_counts