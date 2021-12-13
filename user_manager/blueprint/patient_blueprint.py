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
        self.add_url_rule('/patients/get',
                          'get patient',
                          self.patient_obj.get_patient_by_id,
                          methods=['GET'])
        self.add_url_rule('/patient/details',
                          'get patient details',
                          self.patient_obj.get_patient_details_by_id,
                          methods=['GET'])
        self.add_url_rule('/patients',
                          'all patients',
                          self.patient_obj.patients,
                          methods=['GET'])
        self.add_url_rule('/patients/patients_list',
                          'Filtered list or a list of all patients',
                          self.patient_obj.patients_list,
                          methods=['POST'])
        self.add_url_rule('/patients/add/device',
                          'assign device to patient',
                          self.patient_obj.assign_device,
                          methods=['POST'])
        self.add_url_rule('/patient/device/get',
                          'patient device list',
                          self.patient_obj.patient_device_list,
                          methods=['GET'])
        self.add_url_rule('/patients/<patient_id>/therapy_report_details',
                          'patient therapy report details',
                          self.patient_obj.therapy_report_details,
                          methods=['GET'])
        self.add_url_rule('/patient/device',
                          'disassociate device from patient',
                          self.patient_obj.patient_remove_device,
                          methods=['DELETE'])
