from flask import Blueprint
from resources.patient_manager import PatientManager


class PatientBluePrint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.patient_obj = PatientManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/patients',
                          'create patient',
                          self.patient_obj.create_patient,
                          methods=['POST'])
        self.add_url_rule('/patients',
                          'update patient',
                          self.patient_obj.update_patient,
                          methods=['PUT'])
        self.add_url_rule('/patients',
                          'delete patient',
                          self.patient_obj.delete_patient,
                          methods=['DELETE'])
        self.add_url_rule('/patients/add/device',
                          'assign device to patient',
                          self.patient_obj.assign_device,
                          methods=['POST'])
        self.add_url_rule('/patient/device/get',
                          'patient device list',
                          self.patient_obj.patient_device_list,
                          methods=['GET'])
        '''------------------------ Facility Endpoint -------------------------'''
        self.add_url_rule('/add/facility',
                          'Add Facility',
                          self.patient_obj.add_facility,
                          methods=['POST'])
