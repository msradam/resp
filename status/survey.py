"""
sources:
https://www.annualreviews.org/doi/full/10.1146/annurev-publhealth-032013-182435#_i11
https://www.sciencedirect.com/science/article/pii/S0013935115001255

The common risk factors that increase negative mental health outcomes in response to natural disasters
include pre-existing factors and post-disaster factors. Pre-existing factors include prior mental illness, 
being female, being a child, having children, low socioeconomic status, minority status, and low social connectivity.
Peri-disaster factors include being directly affected by the disaster, intensity of the disaster, and 
death toll of the disaster. Post-disaster factors include property damage, displacement, and job availability.

Our team has sorted these factors into individual and community factors. For simplicity and time, our team has paired 
these factors down to: 

individual risk factors: female, young, minority status, has children (asking about prior mental illness could seem invasive)

general risk factors: displacement, low socio-economic status, low social connectivity, intensity of disaster,
death toll, and job availability (directly affected can be assumed)

You can imagine scaling this analysis to the other factors, as new data is made available.

"In particular relocation and household income were the most predictive factors (for mental wellness)"
"""

import json
import requests
import pandas as pd

from datetime import datetime

from ibm_watson import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='8inyhsDI500GJkL2vcnceEZsUzjJd0n6HvdX_WrtJaHt',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)


def assess_general_risk(origin):
    country = origin["Country"]
    city = origin["City"]

    displacement = pd.read_csv("homeless-natural-disasters.csv")
    death_toll = pd.read_csv("deaths-natural-disasters.csv")
    cities_by_pop = "cities_by_pop.htm".find('#Cities_by_population_density')

    # parse (off-line) data based on survivor's location to assess general population risk

    return


def assess_individual_risk(individual):

    female = individual["Individual"]["gender_identity"].lower() in [
        'female', 'f', 'woman', 'girl']

    [m1, d1, y1] = [individual["Individual"]["birth_month"],
                    individual["Individual"]["birth_day"], individual["Individual"]["birth_year"]]
    [m2, d2, y2] = datetime.today().strftime('%m/%d/%Y').split('/')
    if int(m2) > int(m1) or (int(m2) == int(m1) and int(d2) >= int(d1)):
        age = int(y2) - int(y1)
    else:
        age = int(y2) - int(y1) - 1

    young = age < 16

    responses_to_analyze = ''
    for question in individual['Wellbeing']:
        if question != 'a2' and question[0] == 'a':
            responses_to_analyze += (individual['Wellbeing'][question] + ' ')

    tone = tone_analyzer.tone(
        {'text': responses_to_analyze}, content_type='application/json').get_result()

    sentiment_index = {}

    neg_moods = ["anger", "fear", "sadness", "tentative"]

    for mood in tone["document_tone"]["tones"]:
        if mood["tone_id"] in neg_moods and mood["score"] < 0.85:
            sentiment_index[mood["tone_id"]] = mood["score"]
        if mood["tone_id"] in neg_moods and mood["score"] >= 0.85:
            sentiment_index['intense ' + mood["tone_id"]] = mood["score"]

    wellness_score = 0
    for key in sentiment_index:
        wellness_score += sentiment_index[key]

    wellness_score = (wellness_score/len(sentiment_index)) * \
        (len(sentiment_index)/4)

    factors = []
    if female:
        factors.append('is female')
    if young:
        factors.append('is a child')

    factors = ', '.join(factors)

    if len(sentiment_index.keys()) > 0:
        end_message = ', and is expressing negative sentiments ' + \
            'such as ' + ', '.join(sentiment_index.keys()) + '.'
    else:
        end_message = '.'

    print_outcome = 'This survivor, (' + individual['Individual']['first_name'] + '), shows risk factors associated with poor ' + \
        'mental health outcomes post-disaster: ' + factors + ', their wellness score is ' + str(wellness_score) + ', ' end_message

    idv_data = {'text': responses_to_analyze,
                'anxiety': individual['Feelings']['a1'],
                'guilt': individual['Feelings']['a2'],
                'sadness': individual['Feelings']['a3'],
                'confusion': individual['Feelings']['a4'],
                'fear': individual['Feelings']['a5']}

    return(print_outcome, idv_data, wellness_score)
