# fetchassesment
At home assignment - receipt

INSTRUCTIONS TO RUN DOCKER by building (there is an alternate way of just pulling  uploaded docker from dockerhub and executing):

docker build -t (name) .
docker run -it (name) (there is an infinte docker loop command so there will not be any movement from here on _
open new tab on terminal
docker ps -a (grab the conatiner ID for your docker)
docker exec -it (containerID) sh (using this command you get inside docker)
ls (See if the files are present)
python3 fetchBackend.py (you will prompoted with an IP) (e.g.: http://127.0.0.1:105)
INSTRUCTIONS TO DO DOCKER PULL INSTEAD OF BUILDINB ONE (OPTIONAL DO ONLY IF ABOVE WAY IS NOT DONE):

docker pull monikavarma/backend:finaldemo
docker run -it monikavarma/backend:finaldemo
docker ps -a (get container id)
docker exec -it (containerId) sh
ls (to view all files)
apk upgrade/ update
apk add curl
python3 fetchBackend.py

TESTING ONLY USING CURL:

on a new terminal
do: [ docker ps -a] (grab the conatiner ID for your docker)
docker exec -it (containerID) sh
(you will be prompted with #code inside docker)
apk update
apk add curl
curl --version (to check if curl is installed)
from here you can test:

add curl command to test id generation:
sample curl command:
curl --location --request POST 'http://127.0.0.1:105/receipts/process' 
--header 'Content-Type: application/json' 
--data-raw '{ "retailer": "Target", "purchaseDate": "2022-01-01", "purchaseTime": "13:01",

"items": [ { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },{ "shortDescription": "Emils Cheese Pizza", "price": "12.25" },{ "shortDescription": "Knorr Creamy Chicken", "price": "1.26" },{ "shortDescription": "Doritos Nacho Cheese", "price": "3.35" },{ "shortDescription": " Klarbrunn 12-PK 12 FL OZ ", "price": "12.00" } ], "total": "35.35" }'

you will see points generated on terminal
add curl command to check points calaculated:
sample curl command: curl --location --request GET 'http://127.0.0.1:105/receipts/df9b6eb0-ab0c-11ed-971a-1e00da34dd31/points' 
--header 'Content-Type: application/json' 
--data-raw '{ "retailer": "Target", "purchaseDate": "2022-01-01", "purchaseTime": "13:01", "id": "df9b6eb0-ab0c-11ed-971a-1e00da34dd31", "items": [ { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },{ "shortDescription": "Emils Cheese Pizza", "price": "12.25" },{ "shortDescription": "Knorr Creamy Chicken", "price": "1.26" },{ "shortDescription": "Doritos Nacho Cheese", "price": "3.35" },{ "shortDescription": " Klarbrunn 12-PK 12 FL OZ ", "price": "12.00" } ], "total": "35.35" }'
(DO ENSURE ID IS PRESENT IN JSON AND URL ONLY HAS VALUE OF THE ID(KEY:VALUE PAIR AS INT)

you will see points generated on terminal
ALTERNATE METHOD OF TESTING ON LOCAL SYSTEM: (only done locally if to test on docker go to the above method using curl)

python3 FetchReceipts.py
copy url prompted on terminal: sample url: http://127.0.0.1:105
testing id generation using postman:
enusre python code is running
select POST request on postman
add http://127.0.0.1:105/receipts/process as url
add json data in body of raw section
choose format of bosy as JSON
send request
you will see ID on the terminal
testing points generation usinng postman:
enusre python code is running
select GET request on postman
add http://127.0.0.1:105/receipts//points as url (in place of add df9b6eb0-ab0c-11ed-971a-1e00da34dd31)
add json data with id as key value pair in body of raw section
choose format of bosy as JSON
send request
you will see points on the terminal
