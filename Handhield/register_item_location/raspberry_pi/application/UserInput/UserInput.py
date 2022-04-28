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
    '''
        scan barcodes for items and shelf labels
        and create {}
    '''
    def __init__(self):
        self.reset()

    def reset(self):
        self.type = None
        self.value = None
        self.items = []
        self.jobs = []

    def get(self):
        self.value = input('scan\n')
        self.validate_item()
        if self.type == 'item':
            self.items.append(self.value)
            self.type = None
            return

        self.validate_shelf()
        if self.type == 'shelf':
            self.prepare_jobs()

    def validate_item(self):
        # we do a simple check for lenght before checking if numeric with regex
        l = len(self.value)
        if l > 13 or l < 8:
            return
        # if at this point, we check with regex
        if re.search(REGEX_ITEM, self.value):
            self.type = 'item'

    def validate_shelf(self):
        # force all caps
        self.value = self.value.upper()
        # code128 barcodes reads - as +, we revert this here if that is the case
        self.value = self.value.replace('+', '-')
        if re.search(REGEX_SHELF, self.value):
            self.type = 'shelf'

    def prepare_jobs(self):
        for item in self.items:
            job = {
                'item': item,
                'shelf': self.value,
                'status': '0',
            }
            self.jobs.append(job)
