import re

REGEX_SHELF = '^[A-Z0-9]{1,2}[-][A-Z]{1}[-][0-9]+$'
# first part must be character or numeric (max 2)
# second part must be '-'
# third part must be character (max 1)
# fourth part must be '-'
# fifth and final part must be numeric (unlimited)

REGEX_ITEM = '^[0-9]*$'
# any symbol must be numeric


class UserInput:
    def __init__(self):
        self.type = None
        self.value = None
        self.valid = None
        self.is_item = None
        self.is_shelf = None

    def item(self):
        self.type = None
        self.is_item = False
        self.value = input('scan item\n')
        self.validate_item()

    def validate_item(self):
        # we do a simple check for lenght before checking if numeric with regex
        l = len(self.value)
        if l > 13 or l < 8:
            return
        # if at this point, we check with regex
        if re.search(REGEX_ITEM, self.value):
            self.is_item = True
            self.type = 'item'

    def shelf(self):
        self.type = None
        self.is_shelf = False
        value = input('scan shelf\n').upper()
        # code128 barcodes reads - as +, we revert this here if that is the case
        self.value = value.replace('+', '-')
        self.validate_shelf()

    def validate_shelf(self):
        if re.search(REGEX_SHELF, self.value):
            self.is_shelf = True
            self.type = 'shelf'
