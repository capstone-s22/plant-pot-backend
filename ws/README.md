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
			"potId": "0001",
			"data": [
				{
					"field": "sensors.temperature",
					"value": 1.0
				},
				{
					"field": "sensors.nutrientLevel",
					"value": 1.0
				},
				{
					"field": "sensors.waterLevel",
					"value": 1.0
				}
			]
		}
		```

## From Scheduled Task (Backend)
* Update Rewards (daily checkin)
	```json
	{
		"action": "read",
		"data": [
			{
				"field": "reward.coinsReward",
				"potId": "0001",
				"value": 40,
			},
			{
				"field": "reward.leavesReward",
				"potId": "0001",
				"value": 30,
			},
		]
	}
	````

* Daily check-in
	* Request Green Point Value and Streak Value and Last day of Streak
		```json
		{
			"action": "read",
			"data": [
				{
					"field": "greenPointValues",
					"potId": "0001"
				},
			]
		}
		````

	* Update check-in (don't forget to update reward too - see above)
		```json
		{
			"action": "update",
			"data": [
				{
					"field": "checkIn",
					"potId": "0001",
					"value": true
				},
			]
		}
		````

* **Schedule quizzes**


* Plant Care
	* Request latest health status
		```json
		{
			"action": "read",
			"data": [
				{
					"field": "sensors.temperature.toAlert",
					"potId": "0001"
				},
				{
					"field": "sensors.nutrientLevel.toAlert",
					"potId": "0001"
				},
				{
					"field": "sensors.waterLevel.toAlert",
					"potId": "0001"
				},
			],
		}
		```
	* Send received sensor values + health status + reward (if any)
		```json
		{
			"action": "update",
			"data": [
				{
					"field": "sensors.temperature.value",
					"potId": "0001",
					"value": 1.0,
				},
				{
					"field": "sensors.nutrientLevel.value",
					"potId": "0001",
					"value": 1.0,
				},
				{
					"field": "sensors.waterLevel.value",
					"potId": "0001",
					"value": 1.0,
				},
				{
					"field": "sensors.temperature.toAlert",
					"potId": "0001",
					"value": false,
				},
				{
					"field": "sensors.nutrientLevel.toAlert",
					"potId": "0001",
					"value": false,
				},
				{
					"field": "sensors.waterLevel.toAlert",
					"potId": "0001",
					"value": false,
				},
			],
		}
		```

## From Backend to Pot

* Acknowledgement (for every messages sent to Pot)
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

	* To indicate ready for harvest
		```json
		{
			"action": "update",
			"potId": "1111111",
			"data":[
				{
					"field":"harvest",
					"value":"Pot 1111111's plants are ready to harvest!"
				}
			]
		}

* Rewards sound (daily check-in / quiz)
	* Leaves sound effect
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"alertLeavesSound",
					"value":true
				}
			]
		}

	* Leaves coins effect
		```json
		{
			"action":"update",
			"potId":"1111111",
			"data":[
				{
					"field":"alertCoinsSound",
					"value":true
				}
			]
		}

* Alert checkIn
	* Leaves sound effect
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

* Alert Quiz
	* Leaves sound effect
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



