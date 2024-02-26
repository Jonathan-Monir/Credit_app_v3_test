import pandas as pd
from contract import Contract

class Invoice:
    def __init__(self, df, offers_dict):
        self.df = df
        self.statment = self.df.statment
        self.contracts_sheets = self.df.contracts_sheets
        self.contract_activity = self.df.contracts_activity
        self.offers_dict = offers_dict
        self.metrices = self.invoicesMetrics()
        self.prices = self.metrices[0]
        self.Index_contract_date_range_dict = self.metrices[1]

        
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

    def optimize_invoice_offers(self, index, invoice, contract_name, contract_object, date_range, last_day_removal=True):
        if last_day_removal:
            date_range.loc[len(date_range)-1,"second date"] = date_range.loc[len(date_range)-1,"second date"] - pd.to_timedelta(1, unit='d')
        
        date_range["earlyBooking1"] = 0
        date_range["earlyBooking2"] = 0
        date_range["longTerm"] = 0
        date_range["reduction1"] = 0
        date_range["reduction2"] = 0
        date_range["Nights"] = (date_range["second date"] - date_range["first date"]) + pd.to_timedelta(1, unit='d')
        date_range["price"] = (date_range["Nights"].dt.days * date_range[invoice["Rate code"]]).astype(float)

        
        invoice["earlyBooking1"] = 0
        invoice["earlyBooking2"] = 0
        invoice["longTerm"] = 0
        invoice["reduction1"] = 0
        invoice["reduction2"] = 0

        # Offers
        if contract_object.EarlyBooking1["enable"]:
            invoice["earlyBooking1"] = (invoice["Res_date"] <= contract_object.EarlyBooking1["date"]) * (contract_object.EarlyBooking1["percentage"]/100)
        date_range["earlyBooking1"] = -(invoice["earlyBooking1"] * date_range["price"])

        if contract_object.EarlyBooking2["enable"]:
            invoice["earlyBooking2"] = (invoice["Res_date"] < contract_object.EarlyBooking2["date"] and invoice["Res_date"] > contract_object.EarlyBooking1["date"]) * (contract_object.EarlyBooking2["percentage"]/100)
        date_range["earlyBooking2"] = -(invoice["earlyBooking2"] * date_range["price"])

        if contract_object.LongTerm["enable"]:
            invoice["longTerm"] = ((invoice["Arrival"] - invoice["Departure"]).days >= contract_object.LongTerm["days"]) * (contract_object.LongTerm["percentage"]/100)
        date_range["longTerm"] = -(invoice["longTerm"] * date_range["price"])

        if contract_object.Reduction1["enable"]:
            invoice[contract_object.Reduction1["column"]] = invoice[contract_object.Reduction1["column"]].lower().map({'yes': 1, 'no': 0})

            invoice["Reduction1"] = (invoice[contract_object.Reduction1["column"]] * (contract_object.Reduction1["percentage"]/100))
        date_range["reduction1"] = -(invoice["Reduction1"] * date_range["price"])


        if contract_object.Reduction2["enable"]:
            invoice[contract_object.Reduction2["column"]] = invoice[contract_object.Reduction2["column"]].lower().map({'yes': 1, 'no': 0})
            
            invoice["Reduction2"] = (invoice[contract_object.Reduction2["column"]] * (contract_object.Reduction2["percentage"]/100))
        date_range["reduction2"] = -(invoice["Reduction2"] * date_range["price"])

        
        if contract_object.senior["enable"]:
            invoice[contract_object.senior["column"]] = invoice[contract_object.senior["column"]].lower().map({'yes': 1, 'no': 0})
            
            invoice["senior"] = (invoice[contract_object.senior["column"]] * (contract_object.senior["percentage"]/100))
        date_range["senior"] = -(invoice["senior"] * date_range["price"])

        date_range["price with offers"] = date_range["price"] + date_range["earlyBooking1"] + date_range["earlyBooking2"] + date_range["longTerm"]
        date_range["total price"] = date_range["price"] + date_range["earlyBooking1"] + date_range["earlyBooking2"] + date_range["longTerm"]
        date_range["total price"] = sum(date_range["total price"])
        date_range["contract name"] = contract_name
        return date_range

    def invoicesMetrics(self):
        index_price_dict = {}
        Index_contract_date_range_dict = {}

        for index, invoice in self.statment.iterrows():
            contract_date_range_dict = {}
            rate_code = invoice["Rate code"]
            date_range = pd.DataFrame(columns=["first date","second date",])
            
            
            if self.statment.loc[index,"activity"]:
                self.statment.loc[index,"error_type"]
                while((invoice["Departure"]-invoice["Arrival"]).days != 0):
                    
                    for contract_name, contract_object in reversed(self.offers_dict.items()):
                        if (invoice["Departure"]-invoice["Arrival"]).days == 0:
                            break
                        if invoice["Res_date"] >= contract_object.start_date and invoice["Res_date"] <= contract_object.end_date:
                            
                            # contract not active
                            
                            if not(contract_object.activity):
                                self.statment.loc[index,"activity"] = 0
                                
                                if (self.statment.loc[index,"error_type"]):
                                    self.statment.loc[index,"error_type"] += ", "
                                self.statment.loc[index,"error_type"] += f"error in it's contract ({contract_name})"
                                
                                break
                            
                            # rate code not in contract
                            if not(invoice["Rate code"] in contract_object.contract_sheet.columns):
                                
                                self.statment.loc[index,"activity"] = 0
                                
                                if (self.statment.loc[index,"error_type"]):
                                    self.statment.loc[index,"error_type"] += ", "
                                self.statment.loc[index,"error_type"] += "error in rate code"
                                
                                break
                            
                            new_date_range,invoice = self.oneContractDates(invoice,contract_object.contract_sheet)
                                
                            date_range = pd.merge(date_range,new_date_range, how='outer')

                            new_date_range = self.optimize_invoice_offers(index, invoice, contract_name, contract_object, new_date_range, False)
                            
                            contract_date_range_dict[contract_name] = new_date_range
                            

                            
                            
                            if ((invoice["Departure"]-invoice["Arrival"]).days == 0):
                                date_range = self.optimize_invoice_offers(index, invoice, contract_name, contract_object, date_range, True)

                                new_date_range = self.optimize_invoice_offers(index, invoice, contract_name, contract_object, new_date_range)

                                contract_date_range_dict[contract_name] = new_date_range
                                
                                
                                Index_contract_date_range_dict[index] = contract_date_range_dict
                                
                                index_price_dict[index] = date_range["total price"][0]
                                
                                continue
                    
                    if not(index in index_price_dict) and self.statment.loc[index,"activity"] == 1:
                        self.statment.loc[index,"error_type"] += "reservation date not valid"
                        self.statment.loc[index,"activity"] = 0
                    break
                

                # by arrival
                if (contract_object.sbi["enable"]) and (invoice["Res_date"] >= contract_object.start_date and invoice["Res_date"] <= contract_object.end_date) and (invoice["Departure"] >= contract_object.contract_sheet["first date"][0] and invoice["Arrival"] <= contract_object.contract_sheet["second date"][-1]):
                    
                    date_range = contract_object.contract_sheet[(invoice["Arrival"] <= contract_object.contract_sheet["second date"]) & (invoice["Departure"] >= contract_object.contract_sheet["first date"])].reset_index(drop = True)
                    
                    index_price_dict[index] = (invoice["Departure"] - invoice["Arrival"]) - pd.Timedelta(days=1)
                    
                    
                if self.statment.loc[index,"activity"] == 0:
                    
                    continue
                    
        return index_price_dict, Index_contract_date_range_dict



