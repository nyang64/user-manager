from seeds.users import create_and_register_user, message_details
from seeds.helpers import print_message_details, message_details

from utils.constants import PROVIDER_OUTPATIENT, PROVIDER_PRESCRIBING

from model.providers import Providers

from services.provider_services import ProviderService
from services.facility_services import FacilityService


provider_obj = ProviderService()
facility_obj = FacilityService()


def seed():
    outpatient = create_provider_and_facility(PROVIDER_OUTPATIENT)
    prescribing = create_provider_and_facility(PROVIDER_PRESCRIBING)

    return {"outpatient": outpatient, "prescribing": prescribing}


def create_provider_and_facility(user_details):
    registered_user_id = create_and_register_user(user_details)

    if registered_user_id:
        provider = user_details["provider"]
        facility = provider["facility"]
        facility_address = facility["address"]
        address_id = facility_obj.save_address(facility_address)
        message_details["address"] += f"Address with id '{address_id}' was created. "

        facility_id = facility_obj.save_facility(facility["name"], address_id, facility["on_call_phone"])
        message_details["facility"] += f"Facility with id '{facility_id}' was created. "

        provider_id = provider_obj.add_provider(registered_user_id, facility_id, user_details["provider"]["type"])
        message_details["provider"] += f"Provider with id '{provider_id}' was created. "

        return Providers.find_by_id(provider_id)
    else:
        message_details["provider"] += "Provider was not added. "
        print_message_details()
