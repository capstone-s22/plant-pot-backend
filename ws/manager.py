from validations.schemas import Message, Action, PotData
from ws.pot import new_pot_registration

from lib.firebase import pots_collection

def crud_manager(message: Message):
    try:
        # Create
        if message.action == Action.create:
            for pot_data_dict in message.data:
                # Create Pot
                if pot_data_dict["field"] == PotData.pot:
                    pot_id = pot_data_dict["value"]
                    firestore_input = new_pot_registration(pot_id)
                    pots_collection.document(pot_id).set(firestore_input)
                    return "Pod {} created.".format(pot_id)
        
        # Update
        elif message.action == Action.update:
            pass

        else:
            raise Exception("Invalid Action")
    
    except Exception as e:
        return e

