# Messages Schema 

## From Pot to Backend
* Register pot
	```json
	{
		"action": "create",
		"potId": "0001",
		"data": [
			{
				"field": "pot",
				"value": "0001"
			}
		]
	}
	```

* Daily check-in
	* Get check-in status
		```json
		{
			"action": "read",
			"potId": "0001",
			"data": [
				{
					"field": "showCheckIn",
					"value": "0001"
				}
			]
		}
		```
	* Update check-in action
		```json
		{
			"action": "update",
			"potId": "0001",
			"data": [
				{
					"field": "checkIn",
					"value": true
				}
			]
		}
		```

* Get quiz status
	```json
	{
		"action": "read",
		"potId": "0001",
		"data": [
			{
				"field": "showQuiz",
				"value": "0001"
			}
		]
	}
	```

* Sending encoded images
	```json
	{
		"action": "update",
		"potId": "0001",
		"data": [
			{
				"field": "image",
				"value": "<encoded-image-data>"
			}
		]
	}
	```

* Plant Care
	* Update sensor values
		```json
		{
			"action": "update",
			"potId": "1111111",
			"data": [
				{
					"field": "temperature",
					"value": 25.0
				},
				{
					"field": "nutrientLevel",
					"value": 1000
				},
				{
					"field": "waterLevel",
					"value": 1
				}
			]
		}
		```

## From Backend to Pot

* Acknowledgement (currently only for pot registration)
	```json
	{
		"action": "update",
		"potId": "1111111",
		"data":[
			{
				"field":"ack",
				"value":"<action from prev message to backend> <parameter>"
			}
		]
	}

* Error message 
	```json
	{
		"action": "update",
		"potId": "1111111",
		"data":[
			{
				"field":"error",
				"value":"<error message>"
			}
		]
	}

* Health Check to Pot 
	```json
	{
		"action": "read",
		"potId": "1111111",
		"data":[
			{
				"field":"health check",
				"value":"health check"
			}
		]
	}

* Harvest 
	* To indicate ready for harvest
		```json
		{
			"action": "update",
			"potId": "1111111",
			"data":[
				{
					"field":"showHarvest",
					"value": true
				}
			]
		}
	* Send image over (to perform CV and check if harvested)
		```json
		{
			"action": "read",
			"potId": "1111111",
			"data":[
				{
					"field":"image",
					"value":"send image over"
				}
			]
		}

* Alert checkIn
	* Turn on check-in alert
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"showCheckIn",
					"value":true
				}
			]
		}
	* Turn off check-in alert
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"showCheckIn",
					"value": false
				}
			]
		}

* Alert Quiz
	* Turn on quiz alert
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"showQuiz",
					"value":true
				}
			]
		}
	* Turn off quiz alert
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"showQuiz",
					"value":false
				}
			]
		}

* Alert temperature, EC, water level sensors
	* Turn on sensors alert
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data": [
				{
					"field": "showTemperature",
					"value": true
				},
				{
					"field": "showNutrientLevel",
					"value": true
				},
				{
					"field": "showWaterLevel",
					"value": true
				}
			]
		}
	* Turn off sensors alert
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data": [
				{
					"field": "showTemperature",
					"value": false
				},
				{
					"field": "showNutrientLevel",
					"value": false
				},
				{
					"field": "showWaterLevel",
					"value": false
				}
			]
		}

* (Special Case) Request for EC Sensor Value
	```json
	{
		"action": "read",
		"potId": "1111111",
		"data":[
			{
				"field": "nutrientLevel",
				"value": "send EC value over"
			}
		]
	}

* Sounds (currently not used)
	* Ring Happy sound (for rewards)
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"ringHappySound",
					"value":true
				}
			]
		}

	* Ring Sad sound
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"ringSadSound",
					"value":true
				}
			]
		}





