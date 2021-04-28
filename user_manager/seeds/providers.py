from model.providers import Providers
from seeds.helpers import message_details, print_message_details
from seeds.seed_data import (
    PROVIDER_OUTPATIENT,
    PROVIDER_OUTPATIENT_2,
    PROVIDER_PRESCRIBING,
)
from seeds.users import create_and_register_user
from services.facility_services import FacilityService
from services.provider_services import ProviderService

provider_obj = ProviderService()
facility_obj = FacilityService()


def seed():
    outpatient = create_provider_and_facility(PROVIDER_OUTPATIENT)
    prescribing = create_provider_and_facility(PROVIDER_PRESCRIBING)
    create_provider_and_facility(PROVIDER_OUTPATIENT_2)

    return {"outpatient": outpatient, "prescribing": prescribing}


def create_provider_and_facility(user_details):
    registered_user_id = create_and_register_user(user_details)

    if registered_user_id:
        provider = user_details["provider"]
        facility = provider["facility"]
        facility_address = facility["address"]
        address_id = facility_obj.save_address(facility_address)
        message_details["address"] += f"Address with id '{address_id}' was created. "

        facility_id = facility_obj.save_facility(
            facility["name"], address_id, facility["on_call_phone"]
        )
        message_details["facility"] += f"Facility with id '{facility_id}' was created. "

        provider_id = provider_obj.add_provider(
            registered_user_id, facility_id, user_details["provider"]["role_name"]
        )
        message_details["provider"] += f"Provider with id '{provider_id}' was created. "

        return Providers.find_by_id(provider_id)
    else:
        message_details["provider"] += "Provider was not added. "
        print_message_details()
