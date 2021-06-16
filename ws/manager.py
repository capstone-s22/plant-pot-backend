from ws.pot import new_pot_registration
from validations.schemas import Message, Action, PotDataStr, PotDataBool, PotDataInt, PotDataDictStr, PotDataDictBool, PotDataDictInt 
from lib.firebase import pots_collection

def crud_manager(message: Message):
    pot_id = message.potId
    print(message)
    try:
        # Create
        if message.action == Action.create:
            for pot_data_dict in message.data:
                # Create Pot
                if pot_data_dict["field"] == PotDataStr.pot:
                    pot_id_to_create = pot_data_dict["value"]
                    firestore_input = new_pot_registration(pot_id_to_create)
                    pots_collection.document(pot_id).set(firestore_input)
            return "Pod {} created.".format(pot_id)
        
        # Update
        elif message.action == Action.update:
            for pot_data_dict in message.data:
                # Update check-in
                if pot_data_dict["field"] == PotDataBool.checkIn:
                    parameter = "checkIn"
                    show_check_in = pot_data_dict["value"]
                    # TODO: Retrieve latest session if keeping track
                    firestore_input = {"sessions.1.checkIn.showCheckIn".format() : show_check_in}
                    pots_collection.document(pot_id).update(firestore_input)

                # Update sensor values
                elif pot_data_dict["field"] in [sensor for sensor in PotDataInt]:
                    parameter = "Sensor values"
                    sensor_value = pot_data_dict["value"]
                    # TODO: Retrieve latest session if keeping track
                    firestore_input = {"sessions.1.{}.value".format(pot_data_dict["field"]) : sensor_value}
                    pots_collection.document(pot_id).update(firestore_input)

            return "{} for Pot {} updated.".format(parameter, pot_id)
            # return "{} for Pot {} changed to {}.".format(pot_data_dict["field"], pot_id, sensor_value)


        else:
            raise Exception("Invalid Action")
    
    except Exception as e:
        return e

