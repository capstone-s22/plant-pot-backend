# plant-pot-backend

## To start:
* Create virtual environment
* Download and install requirements `pip3 install requirements.txt`
* Run Flask app in development mode: `python3 app.py`

## Data sample:

```json
{
    "0001": {
        "id": "0001",
        "registered": false,
        "ambient_temp": {
            "25 May 2021 12:00:00 AM": 24.5,
            "25 May 2021 12:00:01 AM": 24.5
        }, 
        "nutrient_level": {
            "25 May 2021 12:00:00 AM":  0.7
        },
        "green_point_score": {
            "25 May 2021 12:00:00 AM":  0.5
        },
        "water_level": {
            "25 May 2021 12:00:00 AM":  0.4
        },
        "isHealthy": {
            "25 May 2021 12:00:00 AM":  0.7
        },
        "toRing": {
            "25 May 2021 12:00:00 AM":  true
        }
    }
}
```

### Dataset changes

Register Pot (POST):
* /add
```json
{
    "0001": {
        "id": "0001",
        "registered": false, // to change to 'true' once registered
        "ambient_temp": {}, 
        "nutrient_level": {}, 
        "green_point_score": {}, 
        "water_level": {}, 
        "isHealthy": {}, 
        "toRing": false, 
    }
}
```

Update parameters (PATCH):
* /update/<parameter>

```json
{
    "0001": {
        "id": "0001",
        "registered": true, 
        "ambient_temp": {}, 
        "nutrient_level": {
            "25 May 2021 12:00:00 AM":  0.7,
        },
        "green_point_score": {}, 
        "water_level": {}, 
        "isHealthy": {}, 
        "toRing": {}, 
    }
}
```

References:
* [HTTP METHODS in REST](https://stackoverflow.com/questions/31089221/what-is-the-difference-between-put-post-and-patch)
