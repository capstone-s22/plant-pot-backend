# plant-pot-backend

## To start:
* Create virtual environment
* Download and install requirements `pip3 install requirements.txt`
* Run Flask app in development mode: `python3 app.py`

## To launch in Heroku:
* Encode Firebase credentials: 
`openssl base64 -A -in plant-pot-firebase-admin.json`
* Once app is deployed to Heroku, with Heroku CLI:
 `heroku config:set FIREBASE_CRED_ENCODED="<encoded-firebase-credentials>"`
 * Ensure environement variable is set through:
 `heroku config -a plant-pot-backend`
 * App should restart. Check if app is launched and connected to Firebase correctly through: 
 `heroku logs -a plant-pot-backend`

 ## To connect to backend (in Heroku) and database (Cloud Firestore)
 * Backend url: https://plant-pot-backend.herokuapp.com
 * Send HTTP requests:
    * Register Pot (POST): https://plant-pot-backend.herokuapp.com/add
        Send JSON request data, e.g.
        ```json
        {
            "0001": {
                "id": "0001",
            }
        }
        ```
    * Update parameters (PUT): https://plant-pot-backend.herokuapp.com/update
        Send JSON request data, e.g.
        ```json
        {
            "id": "0004",
            "parameter": "NutrientLevel", 
            "value": 0.8
        }
        ```

## Data schema for each plant pot (document):
```json
{
    "0001": {
        "ID": "0001",
        "PotRegisteredTime": "30/05/2021 18:32:03",
        "AmbientTemperature": {
            "25 May 2021 12:00:00 AM": 24.5,
            "25 May 2021 12:00:01 AM": 24.5
        }, 
        "NutrientLevel": {
            "25 May 2021 12:00:00 AM":  0.7
        },
        "WaterLevel": {
            "25 May 2021 12:00:00 AM":  0.4
        },
        "GreenPointScore": {
            "Plant1" :{
                "25 May 2021 12:00:00 AM":  0.5
            },
            "Plant2" :{
                "25 May 2021 12:00:00 AM":  0.5
            },
            "Plant3" :{
                "25 May 2021 12:00:00 AM":  0.5
            },
            "Plant4" :{
                "25 May 2021 12:00:00 AM":  0.4
            }
        },
        "IsPlantHealthy": {
            "Plant1" :{
                "25 May 2021 12:00:00 AM":  true
            },
            "Plant2" :{
                "25 May 2021 12:00:00 AM":  true
            },
            "Plant3" :{
                "25 May 2021 12:00:00 AM":  true
            },
            "Plant4" :{
                "25 May 2021 12:00:00 AM":  false
            }        
        },
        "ToRing": {
            "25 May 2021 12:00:00 AM":  true
        },
        "HasCheckedIn": {
            "25 May 2021":  "09:00:00 AM",
            "26 May 2021":  "10:00:00 AM",
            "27 May 2021":  "10:00:00 AM",
            "27 May 2021":  null,
        }
        
    }
}
```


References:
* [HTTP METHODS in REST](https://stackoverflow.com/questions/31089221/what-is-the-difference-between-put-post-and-patch)
* [Deploying Firebase App with Service Account to Heroku](https://stackoverflow.com/questions/41287108/deploying-firebase-app-with-service-account-to-heroku-environment-variables-wit)