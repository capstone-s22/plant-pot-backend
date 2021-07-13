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



