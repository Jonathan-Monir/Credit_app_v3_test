import pandas as pd
class Contract:
    eb1 = {"enable":False,"percentage":10,"date":pd.to_datetime("01/11/2026")}
    eb2 = {"enable":False,"percentage":10,"date":pd.to_datetime("01/11/2026")}
    lt = {"enable":False,"percentage":10,"days":3}
    senior = {"enable":False,"column":"contract","percentage":10}
    reduc1 = {"enable":False,"column":"contract","percentage":10}
    reduc2 = {"enable":False,"column":"contract","percentage":10}
    extra = {"enable":False,"amount":100}
    combinations = {"eb_lt":False,"eb_reduc":True}

    def __init__(self, contract_name, contract_sheet, activity, Senior=senior, EarlyBooking1=eb1, EarlyBooking2=eb2, LongTerm=lt, Reduction1=reduc1, Reduction2=reduc2, combinations=combinations, start_date=None, end_date=None):
        


        self.contract_name = contract_name
        self.contract_sheet = contract_sheet
        self.EarlyBooking1 = EarlyBooking1
        self.Senior = Senior
        self.EarlyBooking2 = EarlyBooking2
        self.LongTerm = LongTerm
        self.Reduction1 = Reduction1
        self.Reduction2 = Reduction2
        self.combinations = combinations
        self.activity = activity
        
        self.start_date = start_date if start_date is not None else self.contract_sheet.loc[0,"first date"]
        self.end_date = end_date if end_date is not None else self.contract_sheet.loc[len(contract_sheet)-1,"second date"]

    

