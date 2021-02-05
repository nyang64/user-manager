from facility.operations.facilities_operations import FacilitiesRepository
from user_address.operations.address_operations import AddressRepository
from role.operations.user_role import RoleRepository

class initializeDB():

    def __init__(self):
        # add_id = self.initAddress()
        # self.initFacility(add_id, "Indore")
        self.initRole()

    def initAddress(self):
        addressRepository = AddressRepository()
        address_id = addressRepository.save_address(
                None, None,
                None, None, None, None, None
            )
        return address_id

    def initFacility(self, address_id, name):
        facility = FacilitiesRepository()
        facility_id = facility.save_facility(address_id, name)

    def initRole(self):
        role = RoleRepository()
        role.save_Role('Admin')
        role.save_Role('Patient')
        role.save_Role('Provider')
