# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    
     ##added the below 4 lines only - 12/19
    if req.get("result").get("action") == "EvalContext":
        result = req.get("result")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        bankname = parameters.get("bank-name") 
        lat_s = {'India Bazaar':'43.0718 N','Walter B Allen': '37.3688 W','Ames Construction':'32.7767 N'} 
        lon_s= {'India Bazaar':'70.7626 N','Walter B Allen': '122.0363 W','Ames Construction':'96.7970 W'}   
        earth_s= {'India Bazaar':'0','Walter B Allen': '1593','Ames Construction':'195'}  
        hyd_s= {'India Bazaar':'10','Walter B Allen': '22','Ames Construction':'19'}
        fld_s ={'India Bazaar':'2','Walter B Allen': '11','Ames Construction':'94'}  
        roof_s ={'India Bazaar':'20','Walter B Allen': '15','Ames Construction':'6'}
        snow_s ={'India Bazaar':'0','Walter B Allen': '15','Ames Construction':'0'}
        fire_s ={'India Bazaar':'20','Walter B Allen': '15','Ames Construction':'6'}
        #fico_str = "Property Risk for " + bankname + " is \n" + "Latitude   : " + str(lat_s[bankname]) + "\n"  + "Longitude   : " + str(lon_s[bankname])+ "Roof Age    : " + str(roof_s[bankname])" years " + "Distance of Property from Firestation   : " + str(fico_score[bankname])" mins "+ "Earth Quake Risk  : " + str(earth_s[bankname])" counts in last 15 years" + "Flood Risk  : " + str(fld_s[bankname])+ "Hail  Risk  : " + str(hail_s[bankname]) + "Fire  Risk  : " + str(fire_s[bankname])         
        fico_str = "Property Risk for " + bankname + " is \n" + "Latitude   : " + str(lat_s[bankname]) + "\n"  + "Longitude   : " + str(lon_s[bankname]) + \
                   "Roof Age    : " + str(roof_s[bankname])+ " years " + " Distance of Property from Firestation   : " + str(fico_score[bankname]) + " mins " + \
                   "Earth Quake Risk  : " + str(earth_s[bankname]) + " counts in last 15 years" + "Flood Risk  : " + str(fld_s[bankname])+ "Snow  Storm  : " + str(hail_s[bankname]) + "Fire  Risk  : " + str(fire_s[bankname])
        bankname = fico_str
        res = makeWebhookResult1(fico_str)
        return res
    
    if req.get("result").get("action") == "CreditContext":
        result = req.get("result")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        bankname = parameters.get("bank-name") 
        credit_score = {'India Bazaar':'Good','Walter B Allen': 'Fair','Ames Construction':'Poor'} 
        equi_score = {'India Bazaar':'715','Walter B Allen': '639','Ames Construction':'500'} 
        fico_score = {'India Bazaar':'720','Walter B Allen': '670','Ames Construction':'600'}  
        credit_str = "Credit Risk Assessment for " + bankname + " is \n"+ "Equifax Score " +str(equi_score[bankname])+ "\n FICO    Score " +str(fico_score[bankname])+ "\n Over all Credit Score " +str(credit_score[bankname]) 
        bankname = credit_str
        res = makeWebhookResult1(credit_str)
        return res
    
    if req.get("result").get("action") == "FicoContext":
        result = req.get("result")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        bankname = parameters.get("bank-name") 
        credit_score = {'India Bazaar':'Good','Walter B Allen': 'Fair','Ames Construction':'Poor'}         
        credit_str = "Associate " + bankname + " seems to have " + str(credit_score[bankname]) + "   Credit"
        bankname = credit_str
        res = makeWebhookResult1(credit_str)
        return res
    
    if req.get("result").get("action") == "yahooWeatherForecast":
        result = req.get("result")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        bankname = parameters.get("bank-name") 
        city_score = {'Yetive Edmonds':'Portsmouth','Walter B Allen': 'Sunnyvale','Ames Construction':'Dover'}  
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query1 = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + str(city_score[bankname]) + "')"
        if yql_query1 is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query1}) + "&format=json"
        result = urlopen(yql_url).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res
    
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
   
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
       return {}
    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    #result = urlopen(yql_url).read()
    #data = json.loads(result)
    #res = makeWebhookResult(data)
    res = makeWebhookResult1(yql_query)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    bankname = parameters.get("bank-name")   
    #if city is None:
    #    return None

    #return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
    return bankname


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeWebhookResult1(bankname):
 
    speech =  bankname

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
