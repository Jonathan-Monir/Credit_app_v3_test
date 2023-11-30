
class InvoiceMapping:
    def __init__(self, statment):
        self.statment =  statment
        self.start = statment.loc[0, "first date"]
        self.end = statment.loc[0, "second date"]
    def valid_dates(self, Contracts):
        
        pass