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
* Rewards sound (daily check-in / quiz)
	* Leaves sound effect
		```json
		{
			"action": "update",
			"data": [
				{
					"field": "alertLeavesSound",
					"potId": "0001",
					"value": true
				}
			]
		}

	* Leaves coins effect
		```json
		{
			"action": "update",
			"data": [
				{
					"field": "alertCoinsSound",
					"potId": "0001",
					"value": true
				}
			]
		}
* Plant Care
	* Update toAlert
		```json
		{
			"action": "update",
			"data": [
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
			]
		}
