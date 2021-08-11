# plant-pot-backend

## To start:
* Create virtual environment
* Download and install requirements `pip3 install requirements.txt`
* Run FastAPI app in development mode: `uvicorn main:app --reload --port 8000`

## To launch in Heroku:
* Encode Firebase credentials: 
`openssl base64 -A -in plant-pot-firebase-admin.json`
* Once app is deployed to Heroku, with Heroku CLI:
 `heroku config:set FIREBASE_CRED_ENCODED="<encoded-firebase-credentials>"`
 `heroku config:set CV_SERVER_URL_PREFIX="<CV-server-URL>"`

 * Ensure environement variable is set through:
 `heroku config -a plant-pot-backend`
 * App should restart. Check if app is launched and connected to Firebase correctly through: 
 `heroku logs -a plant-pot-backend`
