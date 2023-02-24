"""
@author: Monika Varma
Version: 02/22/2023
python code to generate id and calculate points for json object
"""

import uuid
import math
from flask import Flask
from flask import request
from datetime import datetime
from flask import Flask, abort
from flask import jsonify
from flask import Flask, render_template

app = Flask(__name__)  # create an instance of flask

"""
@path: '/receipts/process'
sample test url: http://127.0.0.1:105/receipts/points
run python code
in a new terminal go to the file directory and post the curl command in the terminal you will receive a dict object with Id
"""
@app.errorhandler(404) 
def invalid_route(e): 
    return jsonify({'errorCode' : 404, 'message' : 'Route not found'})

@app.errorhandler(500) 
def invalid_route(e): 
    return jsonify({'errorCode' : 500, 'message' : 'error with server'})


@app.route('/receipts/process', methods=['GET', 'POST'])  # trigger url at '/receipts/process' and only post
def generateId():
    try:
        """
        :return: dict: {"id":"uuid"} random id generated for the retailer
        generates an ID if not in existence already for retailer
        """
        if request.method == 'POST':
            content = request.get_json()  # get json data
            if 'id' not in content:
                store_id = uuid.uuid1()  # use uuid to generate id
                content['id'] = store_id
                return {'id': store_id}
            else:
                
                return jsonify({'errorCode' : 400, 'Error' : 'Json has ID'})

        else:
            
            return jsonify({'errorCode' : 400, 'Error' : 'only POST method allowed'})
    except:
        
        return jsonify({'errorCode' : 404, 'Error' : 'Check Url Invalid/Bad request'})


"""
@path: '/receipts/<id>/points'
sample test url: http://127.0.0.1:105/receipts/5a03c46d-ab0a-11ed-b96f-0242ac110004/points
[IMP: JSON HERE SHOULD HAVE ID AS KEY VALUE PAIR AND URL SHOULD ONLY HAVE THE VALUE OF ID NOT THE KEY AS INT]              
run python code                                                                                                            
in a new terminal go to the file directory and post the curl command in the terminal you will receive points for the JSON object
"""


@app.route('/receipts/<id>/points', methods=['GET', 'POST'])  # trigger url at '/receipts/{id}/points' and only get
def points(id):
    """
    :param id: the ID passed in URL and present in JSON
    :return: dict: {"points":"int"} points calculated based on all rules for json object with this ID
    calculates points awarded based on retailer name, odd purchase date, purchase time, item count, item description and total
    methods generated for each point calculation following single Responsibility principle
    """
    try:
        # validate request
        if request.method == 'GET':
            points_awarded = 0
            try:
                content = request.get_json()  # get json data
            except ValueError as e:
                
                return jsonify({'errorCode' : 400, 'Error' : 'Enter valid JSON'})
            if 'id' not in content:
                
                return jsonify({'errorCode' : 400, 'Error' : 'JSON has no ID'})
            if id != content['id']:
                
                return jsonify({'errorCode' : 400, 'Error' : 'URL and JSON ID do not match'})

            if 'retailer' in content:
                retailer_name = content['retailer']

                # function call to calculate points for retailer name
                points_awarded += retailerNamePoints(retailer_name)
            else:
                
                return jsonify({'errorCode' : 400, 'Error' : 'JSON does not have retailer name'})

            if 'total' in content:
                total_points = content['total']
                total_points = float(total_points)

                # function call to calculate points if total is whole number with no cents
                points_awarded += wholeTotal(total_points)

                # function call to calculate points if total is multiple of 0.25
                points_awarded += multipleOfTotal(total_points)

            else:
                
                return jsonify({'errorCode' : 400, 'Error' : 'JSON does not have total'})

            if 'purchaseTime' in content:
                purchased_time = content['purchaseTime']

                # function call to calculate points if purchase time is between 2pm to 4pm
                points_awarded += checkPurchaseTime(purchased_time)
            else:
                return "Error: JSON does not have purchaseTime", 200

            if 'items' in content:
                items_list = content['items']

                # function call to calculate 5 points for every 2 items
                points_awarded += countItems(items_list)

                # function call to calculate points for short description of items
                points_awarded += countDescPoints(items_list, len(items_list))
            else:
                #return "Error: JSON does not have items", 200
                return jsonify({'errorCode' : 400, 'Error' : 'JSON does not have items'})

            if 'purchaseDate' in content:

                curr_date = content['purchaseDate']

                # function call to calculate points for odd day shopping
                points_awarded += checkPurchaseDate(curr_date)
            else:
                
                return jsonify({'errorCode' : 400, 'Error' : 'JSON does not have puchase date'})

            # return calculated points
            return {'points': points_awarded}
        else:
            
            return jsonify({'errorCode' : 400, 'Error' : 'only GET method allowed'})
    except:
        
        return jsonify({'errorCode' : 404, 'Error' : 'Check Url Invalid/Bad request'})


def retailerNamePoints(retailer_name):
    """
    :param retailer_name: given retailer name in JSON
    :return: temp: points for retailer name
    function  to calculate points for retailer name
    """
    temp = 0
    for char in retailer_name:
        if char.isalnum():
            temp += 1
    return temp


def wholeTotal(total_points):
    """
    :param total_points: given total in JSON
    :return: temp: points if total is whole number with no cents
    calculates points for  total dollar with no cents
    """

    temp = 0
    if total_points.is_integer():
        temp += 50
    return temp


def multipleOfTotal(total_points):
    """
    :param total_points: given total in JSON
    :return: temp: points awarded if total is mutiple of 0.25
    calculates points if total is multiple of 0.25
    """
    temp = 0
    if (total_points % 0.25) == 0:
        temp += 25
    return temp


def checkPurchaseTime(purchased_time):
    """
    :param purchased_time: given purchase time in JSON
    :return: temp: points awarded for time of purchase
    calculates points if purchase time is between 2 -4 pm
    """
    temp = 0
    if '14:00' <= purchased_time <= '15:00':
        temp += 10
    return temp


def countItems(items_list):
    """
    :param items_list: given items in JSON
    :return: temp: points awarded for pair of items
    calculates points for every 2 items
    """
    temp = 0
    items_count = len(items_list)
    temp += 5 * (items_count // 2)
    return temp


def countDescPoints(items_list, items_count):
    """
    :param items_list: Items from JSON
    :param items_count: numbers of items is JSON
    :return: temp: points awarded for odd date purchase
    calculates points based on short description of all items
    """
    i = 0
    temp = 0
    while i < items_count:
        val = list(items_list[i].values())
        item_desc = val[0].strip()
        if len(item_desc) % 3 == 0:
            temp += math.ceil(
                float(val[1]) * 0.2)  # use ceil to round up to higher int value
        i += 1
    return temp


def checkPurchaseDate(curr_date):
    """
    :param curr_date: given purchase date in YY-MM-DD format from JSON
    :return: temp: points awarded for odd date purchase
    calculates points based if date of purchase id odd
    """
    temp = 0
    date_object = datetime.strptime(curr_date, '%Y-%m-%d').date()
    day = date_object.strftime('%d')  # use strftime to get date from date format
    if int(day) % 2 != 0:
        temp += 6
    return temp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)  # run flask on port 105, host 0.0.0.0 makes server accessible locally
