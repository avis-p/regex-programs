import re
def check_num(phone_list):
    rgx_phone = re.compile(r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}")
    
    result = [x for x in phone_list if re.findall(rgx_phone, x)]
    return result
    
phone_list = ["2124567890", "(212)456-7890", "(212)-456-7890", "212.456.7890",
        "212 456 7890", "+12124567890", "+1 212.456.7890", "+212-456-7890", "1-212-456-7890"]

print(check_num(phone_list))

#output
    #['2124567890', '(212)456-7890', '212.456.7890', '212 456 7890', '+12124567890', '+1 212.456.7890', '+212-456-7890', '1-212-456-7890']