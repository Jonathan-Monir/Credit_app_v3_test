import pandas as pd
from contract import Contract

class Invoice:
    def __init__(self, statment, contracts_sheets,contract_activity):
        self.statment = statment
        self.contracts = self.make_contracts_dict(contracts_sheets,contract_activity)

    def oneContractDates(self,invoice, contract):
        first_date = contract.loc[0,"first date"]
        last_date = contract.loc[len(contract)-1,"second date"]
        rate_code = invoice["Rate code"]
        date_range = contract[(invoice["Arrival"] <= contract["second date"]) & (invoice["Departure"] >= contract["first date"])].reset_index(drop = True)
        
        # inside 
        if invoice["Arrival"] >= first_date and invoice["Departure"] <= last_date:
            date_range.loc[0,"first date"] = invoice["Arrival"]
            date_range.loc[len(date_range)-1,"second date"] = invoice["Departure"]

            invoice["Departure"] = invoice["Arrival"] 
        # outside all (arrival < first date), (departure > last date)
        elif invoice["Arrival"] < first_date and invoice["Departure"] > last_date:
            new_invoice = invoice.copy()
            invoice["Departure"] = first_date
            new_invoice["Arrival"] = last_date
            invoice = pd.DataFrame(invoice).transpose()

            invoice.loc[1,:] = new_invoice
        # outside left (arrival < first date)
        elif invoice["Arrival"] < first_date:
            date_range.loc[len(date_range)-1,"second date"] = invoice["Departure"]
            invoice["Departure"] = first_date
        
        #outside right (Departure > last date)
        elif invoice["Departure"] > last_date:
            date_range.loc[0,"first date"] = invoice["Arrival"]
            invoice["Arrival"] = last_date

        

        date_range = date_range[["first date","second date",rate_code]]

        return date_range, invoice

    def make_contracts_dict(self,contracts_sheets,contract_activity):
        contract_dict = {}
        for contract_name, contract_data in contracts_sheets.items():
            contract_dict[contract_name] = Contract(contract_name, contract_data, contract_activity[contract_name])
        return contract_dict

    def allContractsDates(self):

        for index, invoice in self.statment.iterrows():
            rate_code = invoice["Rate code"]
            date_range = pd.DataFrame(columns=["first date","second date",])
            if invoice["activity"]:
                
                while((invoice["Departure"]-invoice["Arrival"]).days != 0):
                    
                    for contract_name, contract_object in reversed(self.contracts.items()):
                        
                        if invoice["Res_date"] >= contract_object.start_date and invoice["Res_date"] <= contract_object.end_date:
                            if not(contract_object.activity):
                                invoice["activity"] = 0
                            new_date_range,invoice = self.oneContractDates(invoice,contract_object.contract_sheet)
                            if index ==29:
                                print(contract_name)
                                print(new_date_range)
                            
                            date_range = pd.merge(date_range,new_date_range, how='outer')

                            if ((invoice["Departure"]-invoice["Arrival"]).days == 0):
                                date_range.loc[len(date_range)-1,"second date"] = date_range.loc[len(date_range)-1,"second date"] - pd.to_timedelta(1, unit='d')
                                date_range["Nights"] = (date_range["second date"] - date_range["first date"]) + pd.to_timedelta(1, unit='d')
                                date_range["total price"] = (date_range["Nights"].dt.days * date_range[rate_code]).astype(float)
                                
                                if index == 29:
                                    print("final date range")
                                    print(date_range)
                                    
                                continue
                                


    def combineDates(self):
        pass

    def checkContractActivity(self):
        pass

    def finalInvoiceDictionary(self):
        pass