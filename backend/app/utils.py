import re
from datetime import datetime

# --- UPI Validation ---
def validate_vpa(vpa: str) -> bool:
    # Pattern: ^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+$
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+$"
    return bool(re.match(pattern, vpa))

# --- Card Validation (Luhn Algorithm) ---
def validate_luhn(card_number: str) -> bool:
    # Remove spaces/dashes
    clean_num = re.sub(r"\D", "", card_number)
    
    if not 13 <= len(clean_num) <= 19:
        return False
        
    digits = [int(d) for d in clean_num]
    checksum = 0
    
    # Process from right to left
    # Double every second digit
    for i in range(len(digits) - 2, -1, -2):
        doubled = digits[i] * 2
        if doubled > 9:
            doubled -= 9
        digits[i] = doubled
        
    checksum = sum(digits)
    return checksum % 10 == 0

# --- Card Network Detection ---
def get_card_network(card_number: str) -> str:
    clean_num = re.sub(r"\D", "", card_number)
    
    if clean_num.startswith("4"):
        return "visa"
    
    # Mastercard: 51-55
    if 51 <= int(clean_num[:2]) <= 55:
        return "mastercard"
    
    # Amex: 34 or 37
    if clean_num[:2] in ["34", "37"]:
        return "amex"
    
    # RuPay: 60, 65, 81-89
    prefix_2 = int(clean_num[:2])
    if prefix_2 in [60, 65] or (81 <= prefix_2 <= 89):
        return "rupay"
        
    return "unknown"

# --- Expiry Validation ---
def validate_expiry(month: str, year: str) -> bool:
    try:
        m = int(month)
        y = int(year)
        
        # Validate Month
        if not (1 <= m <= 12):
            return False
            
        # Handle 2-digit year (assume 20xx)
        if y < 100:
            y += 2000
            
        current_date = datetime.now()
        current_y = current_date.year
        current_m = current_date.month
        
        # Check if future or current month
        if y > current_y:
            return True
        elif y == current_y and m >= current_m:
            return True
            
        return False
    except:
        return False