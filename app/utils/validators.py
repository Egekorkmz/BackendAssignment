import re

class Validators:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        return bool(email_regex.match(email))
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        phone_regex = re.compile(
            r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"
        )
        return bool(phone_regex.match(phone))
    
    @staticmethod
    def is_valid_year(year: str) -> bool:
        year_regex = re.compile(r"^\d{4}$")
        return bool(year_regex.match(year))
    
    @staticmethod
    def is_valid_iso_date(date_str: str) -> bool:
        iso_date_regex = re.compile(
            r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)?$"
        )
        return bool(iso_date_regex.match(date_str))