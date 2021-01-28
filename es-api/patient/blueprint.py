from flask import Blueprint
from patient.patient_operation.patient_manager import PatientManager

class PatientBluePrint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.patientObj = PatientManager()
        self._add_routes()
        
    def _add_routes(self):
        self.add_url_rule('/patients/<id>', 'create patient', self.patientObj.create_patient, methods=['POST'])
        self.add_url_rule('/patients/<id>', 'get patient', self.patientObj.create_patient, methods=['GET'])
        self.add_url_rule('/patients/<id>', 'update patient', self.patientObj.create_patient, methods=['PUT'])
        self.add_url_rule('/patients/<id>', 'delete patient', self.patientObj.create_patient, methods=['DELETE'])
        self.add_url_rule('/patients/device/get', 'patient device list', self.patientObj.patient_device_list, methods=['GET'])