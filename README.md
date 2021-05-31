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
    * Update parameters (PATCH): https://plant-pot-backend.herokuapp.com/update
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
        "GreenPointScore": {
            "25 May 2021 12:00:00 AM":  0.5
        },
        "WaterLevel": {
            "25 May 2021 12:00:00 AM":  0.4
        },
        "IsPlantHealthy": {
            "25 May 2021 12:00:00 AM":  0.7
        },
        "ToRing": {
            "25 May 2021 12:00:00 AM":  true
        }
    }
}
```


References:
* [HTTP METHODS in REST](https://stackoverflow.com/questions/31089221/what-is-the-difference-between-put-post-and-patch)
* [Deploying Firebase App with Service Account to Heroku](https://stackoverflow.com/questions/41287108/deploying-firebase-app-with-service-account-to-heroku-environment-variables-wit)