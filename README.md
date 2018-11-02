#Schonfeld Coding Test Submission
This test is meant to assess your thinking and problem solving skills. You will be building a small web app using docker and python and some libraries that you likely have not used before. Feel free to use google to gain a better understanding of the tooling but please do not have others help you with the project.

Before you submit the project, please test it inside the docker container and make sure it works.

##Testing
To test this project, run `pytest` in the root directory with all dependencies installed. This project was built on python3.6.

##Setup
1) Install and setup docker (https://docs.docker.com/install/)
2) **Optional:** If you would like to develop locally rather than use the docker container for development you will need to setup a python 3.6 environment (https://www.python.org/downloads/release/python-360/).
3) **Optional:** If you would like to use an IDE for python we recommend pycharm (https://www.jetbrains.com/pycharm/download/) 
4) **Optional:** If you would like to use a tool other than cURL for testing your API we recommend Postman (https://www.getpostman.com/apps) 

##Hello World Health Check
Included with this readme are a few base files to help you get started:
 - Dockerfile - This will build a docker image to run your service
 - app.py - This is the entry point for your service and what will drive route configuration
 - health_check.py - A simple health check resource to make sure the service is running as expected
 - requirements.txt - Any dependencies should go in here, line 5 of the Dockerfile will install them for you.
   - falcon is a simple WSGI app framework that handles the boiler plate WSGI requirements (https://falcon.readthedocs.io/en/stable/)
   - gunicorn is the wsgi server that will serve up the WSGI app (https://gunicorn.org/)

From this project directory run: `docker build .`

The last line should output something like: "Successfully build <image_id>". If you run `docker images` you should see that id in the Image ID column

Once you have an image_id you can run `docker run -d -p 8080:8080 <image_id>`. If the container starts up successfully you should be able to go to 127.0.0.1:8080/health

####Questions:
1) What are the -d and -p flags passed into the `docker run` command? 
2) In the /health endpoint there is a hostname attribute. What does that hostname represent?


##Matching Engine
Now that you have a working health check, it's time to build on top of that.

**NOTE:** Be sure to use the correct HTTP verbs for each endpoint
**NOTE:** Be sure to also write tests around the application. Feel free to use any framework you're comfortable with.

**TL;DR** A matching engine is a tool used in trading that matches people that want to buy stocks with people that want to sell them. More specifically, it matches buy orders with sell orders; this is called filling an order.
Here is a link if you want more information: https://en.wikipedia.org/wiki/Order_matching_system

1) Create a new endpoint that takes in "orders" (/orders) and store it in memory. Here is an example data model:
    ```json
    {
        "data":
        {
            "traderId": "skbks-sdk39sd-3ksfl43io3-alkjasf-34",
            "orders":
            [
                {
                    "symbol": "AAPL",
                    "quantity": 100,
                    "orderType": "buy"
                },
                {
                    "symbol": "NVDA",
                    "quantity": 5000,
                    "orderType": "buy"
                },
                {
                    "symbol": "MSFT",
                    "quantity": 2500,
                    "orderType": "sell"
                }
            ]
        }
    }
    ```
   
2) Create an endpoint to view a given trader's current orders and statuses (/orders/<trader_id>). The data model for that should look something like this:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            },
            {
                "symbol": "NVDA",
                "quantity": 5000,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            },
            {
                "symbol": "MSFT",
                "quantity": 2500,
                "orderType": "sell",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            }
        ]
    }
    ```
    
3) Write matching logic to match buy and sell orders. Here is some sample input/output:

    Trader 1 sends in an order like this:
    ```json
    {
        "data":
        {
            "traderId": "trader1",
            "orders":
            [
                {
                    "symbol": "AAPL",
                    "quantity": 100,
                    "orderType": "buy"
                }
            ]
        }
    }
    ```
    
    Then if you hit `/orders/trader1` it should return:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            }
        ]
    }
    ```
    
    And then if Trader 2 sends in something like this:
    ```json
    {
        "data":
        {
            "traderId": "trader2",
            "orders":
            [
                {
                    "symbol": "AAPL",
                    "quantity": 100,
                    "orderType": "sell"
                }
            ]
        }
    }
    ```
    
    and `/orders/trader1` should now look something like this:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "filled"
            }
        ]
    }
    ```
    
    and `/orders/trader2` should look like this:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "sell",
                "orderTime": "2018-10-10 13:35:40.647845",
                "status": "filled"
            }
        ]
    }
    ```
    
