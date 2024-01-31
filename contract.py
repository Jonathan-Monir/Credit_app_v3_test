class Contract:
    
    def __init__(self, contract_name, contract_sheet, activity, EarlyBooking1=0, EarlyBooking2=0, LongTerm=0, Reduction1=0, Reduction2=0, combinations=0, start_date=None, end_date=None):
        
        self.contract_name = contract_name
        self.contract_sheet = contract_sheet
        self.EarlyBooking1 = EarlyBooking1
        self.EarlyBooking2 = EarlyBooking2
        self.LongTerm = LongTerm
        self.Reduction1 = Reduction1
        self.Reduction2 = Reduction2
        self.combinations = combinations
        self.activity = activity
        
        self.start_date = start_date if start_date is not None else self.contract_sheet.loc[0,"first date"]
        self.end_date = end_date if end_date is not None else self.contract_sheet.loc[len(contract_sheet)-1,"second date"]

    

