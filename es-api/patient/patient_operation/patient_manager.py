from flask import jsonify
import http

class PatientManager():
    def __init__(self):
        pass
    
    def create_patient(self):
        pass
    
    def patient_device_list(self):
        devices = [['1212', '12EE', True],
                   ['1213', '13EE', True],
                   ['1512', '12TE', False]]
        device_list = [
            {'serial_number': d[0],
             'key': d[1],
             'status': d[2]
             } for d in devices]
        resp = {'devices':device_list}
        return jsonify(resp), http.client.OK