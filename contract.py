class Contract:
    
    def __init__(self, contract, EarlyBooking1=0, EarlyBooking2=0, LongTerm=0, Reduction1=0, Reduction2=0, combinations=0, start_date=None, end_date=None):
        self.EarlyBooking1 = EarlyBooking1
        self.EarlyBooking2 = EarlyBooking2
        self.LongTerm = LongTerm
        self.Reduction1 = Reduction1
        self.Reduction2 = Reduction2
        self.contract = contract
        self.combinations = combinations

        self.start_date = start_date if start_date is not None else self.contract.loc[0,"first date"]
        self.end_date = end_date if end_date is not None else self.contract.loc[len(contract)-1,"second date"]

    

