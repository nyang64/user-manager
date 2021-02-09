from flask import Blueprint
from patient.patient_operation.patient_manager import PatientManager

class PatientBluePrint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.patientObj = PatientManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/patients',
                          'create patient',
                          self.patientObj.create_patient,
                          methods=['POST'])
        self.add_url_rule('/patients', 'update patient',
                          self.patientObj.update_patient,
                          methods=['PUT'])
        self.add_url_rule('/patients',
                          'delete patient',
                          self.patientObj.delete_patient,
                          methods=['DELETE'])
        self.add_url_rule('/patients/add/device',
                          'assign device to patient',
                          self.patientObj.assign_device,
                          methods=['POST'])
        self.add_url_rule('/patient/device/getlist',
                          'patient device list',
                          self.patientObj.patient_device_list,
                          methods=['GET'])
        self.add_url_rule('/patient/device/get',
                          'mock patient device list',
                          self.patientObj.mock_patient_device_list,
                          methods=['GET'])
