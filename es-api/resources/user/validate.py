def user_input(request_data):
    if 'first_name' not in request_data:
        raise Exception('param first_name is required')
    if 'last_name' not in request_data:
        raise Exception('param last_name is required')
    if 'phone_number' not in request_data:
        raise Exception('param phone_number is required')
    if 'email' not in request_data:
        raise Exception('param email is required')

def is_None(request_data):
    first_name = request_data.get('first_name')
    last_name = request_data.get('last_name')
    phone_number = request_data.get('phone_number')
    email = request_data.get('email')
    
    if first_name is None or first_name == '':
        raise Exception('first_name cannot be None')
    if last_name is None or last_name == '':
        raise Exception('last_name cannot be None')
    if phone_number is None or len(phone_number) == 0:
        raise Exception('phone_number cannot be None')
    if email is None or email == '':
        raise Exception('email cannot be None')
    return first_name, last_name, phone_number, email
    
    