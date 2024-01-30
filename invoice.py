import pandas as pd

class Invoice:
    def __init__(self, statment=0, contracts=0):
        self.statment = statment
        self.contracts = contracts

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

        date_range.loc[len(date_range)-1,"second date"] = date_range.loc[len(date_range)-1,"second date"] - pd.to_timedelta(1, unit='d')
        date_range["Nights"] = (date_range["second date"] - date_range["first date"]) + pd.to_timedelta(1, unit='d')
        date_range["price"] = (date_range["Nights"].dt.days * date_range[rate_code]).astype(float)

        date_range = date_range[["first date","second date",rate_code,"Nights","price"]]

        return date_range, invoice

    def allContractsDates(self):
        pass

    def combineDates(self):
        pass

    def checkContractActivity(self):
        pass

    def finalInvoiceDictionary(self):
        pass