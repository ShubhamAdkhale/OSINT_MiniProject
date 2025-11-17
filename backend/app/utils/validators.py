import phonenumbers
from phonenumbers import NumberParseException

def validate_phone_number(phone_number):
    """
    Validate phone number format
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not phone_number:
        return False, "Phone number is required"
    
    try:
        parsed = phonenumbers.parse(phone_number, None)
        
        if not phonenumbers.is_valid_number(parsed):
            return False, "Invalid phone number format"
        
        return True, None
        
    except NumberParseException as e:
        return False, f"Invalid phone number: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def format_phone_number(phone_number):
    """Format phone number to E.164 standard"""
    try:
        parsed = phonenumbers.parse(phone_number, None)
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except:
        return phone_number
