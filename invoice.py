import pandas as pd
import sqlite3
from contract import Contract
from file_uploader import FileUploader
from contract import Contract
import warnings
from datetime import datetime, timedelta


# Clear the terminal

warnings.filterwarnings("ignore", message="A value is trying to be set on a copy of a slice from a DataFrame.*")

warnings.filterwarnings("ignore")
class Invoice:
    def __init__(self, df, offers_dict=None):
        self.df = df
        self.statment = self.df.statment
        self.contracts_sheets = self.df.contracts_sheets
        self.contract_activity = self.df.contracts_activity
        self.offers_dict = self.make_contracts_dict(self.contracts_sheets, self.contract_activity) if offers_dict is None else offers_dict
        self.metrices = self.invoicesMetrics()
        self.prices = self.metrices[0]
        self.Index_contract_date_range_dict = self.metrices[1]
        self.output_statment = self.metrices[2]

        
    def oneContractDates(self,invoice, contract, index):
        first_date = contract.loc[0,"first date"]
        last_date = contract.loc[len(contract)-1,"second date"]
        rate_code = invoice["Rate code"]
        date_range = contract[(invoice["Arrival"] <= contract["second date"]) & (invoice["Departure"] >= contract["first date"])].reset_index(drop = True)
        valid = True
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
        elif invoice["Arrival"] < first_date and invoice["Departure"] >= first_date:
            date_range.loc[len(date_range)-1,"second date"] = invoice["Departure"]
            invoice["Departure"] = first_date - timedelta(days=1)
        
        #outside right (Departure > last date)
        elif invoice["Departure"] > last_date and invoice["Arrival"]  <=  last_date :
            date_range.loc[0,"first date"] = invoice["Arrival"]
            date_range.loc[len(date_range)-1,"second date"] = date_range.loc[len(date_range)-1,"second date"]
            invoice["Arrival"] = last_date + timedelta(days=1)
            if invoice["Departure"]  == invoice["Arrival"]:
                date_range.loc[len(date_range)-1,"first date"] -= timedelta(days=1) 
            #invoice["Departure"] = invoice["Departure"] + timedelta(days=1)

            
        else:
            valid = False
        date_range = date_range[["first date","second date",rate_code]]

        return date_range, invoice, valid

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
        date_range["Nights"] = (date_range["second date"] - date_range["first date"] + timedelta(days=1))
        date_range["price"] = (date_range["Nights"].dt.days * date_range[invoice["Rate code"]]).astype(float)

        
        invoice["earlyBooking1"] = 0
        invoice["earlyBooking2"] = 0
        invoice["longTerm"] = 0
        invoice["reduction1"] = 0
        invoice["reduction2"] = 0

        # Offers
        if contract_object.EarlyBooking1["enable"]:
            invoice["earlyBooking1"] = (invoice["Res_date"] <= contract_object.EarlyBooking1["date"]) * (int(contract_object.EarlyBooking1["percentage"])/100)
        date_range["earlyBooking1"] = -(invoice["earlyBooking1"] * date_range["price"])

        if contract_object.EarlyBooking2["enable"]:
            invoice["earlyBooking2"] = (invoice["Res_date"] < contract_object.EarlyBooking2["date"] and invoice["Res_date"] > contract_object.EarlyBooking1["date"]) * (int(contract_object.EarlyBooking2["percentage"])/100)
        date_range["earlyBooking2"] = -(invoice["earlyBooking2"] * date_range["price"])

        if contract_object.LongTerm["enable"]:
            invoice["longTerm"] = ((invoice["Arrival"] - invoice["Departure"]).days >= contract_object.LongTerm["days"]) * (int(contract_object.LongTerm["percentage"])/100)
        date_range["longTerm"] = -(invoice["longTerm"] * date_range["price"])

        if contract_object.Reduction1["enable"]:
            invoice[contract_object.Reduction1["column"]] = invoice[contract_object.Reduction1["column"]].lower().map({'yes': 1, 'no': 0})

            invoice["Reduction1"] = (invoice[contract_object.Reduction1["column"]] * (contract_object.Reduction1["percentage"]/100))
        date_range["reduction1"] = -(invoice["Reduction1"] * date_range["price"])


        if contract_object.Reduction2["enable"]:
            invoice[contract_object.Reduction2["column"]] = invoice[contract_object.Reduction2["column"]].lower().map({'yes': 1, 'no': 0})
            
            invoice["Reduction2"] = (invoice[contract_object.Reduction2["column"]] * (int(contract_object.Reduction2["percentage"])/100))
        date_range["reduction2"] = -(invoice["Reduction2"] * date_range["price"])

        
        if contract_object.senior["enable"]:
            invoice["senior room type"] = invoice[contract_object.senior["Rate code"]].apply(self.senior_mapping)

            
            invoice["senior"] = ((invoice[contract_object.senior["column"]]/invoice["senior room type"]) * (contract_object.senior["percentage"]/100))
        date_range["senior"] = -(invoice["senior"] * date_range["price"])

        date_range["price with offers"] = date_range["price"] + date_range["earlyBooking1"] + date_range["earlyBooking2"] + date_range["longTerm"]
        date_range["total price"] = date_range["price"] + date_range["earlyBooking1"] + date_range["earlyBooking2"] + date_range["longTerm"]
        date_range["total price"] = sum(date_range["total price"])
        date_range["contract name"] = contract_name
        return date_range

        
    def senior_mapping(self, value):
        value_lower = value.lower()
        if value_lower.startswith('s'):
            return 1
        elif value_lower.startswith('d'):
            return 2
        elif value_lower.startswith('t'):
            return 3
        elif value_lower.startswith('q'):
            return 4
        else:
            return value  # Return the original value if it doesn't match any condition


    def invoicesMetrics(self):
        index_price_dict = {}
        Index_contract_date_range_dict = {}
        for index, invoice in self.statment.iterrows():
            contract_date_range_dict = {}
            rate_code = invoice["Rate code"]
            date_range = pd.DataFrame(columns=["first date","second date",])
            #invoice["Departure"] = invoice["Departure"] - timedelta(days=1)
            
            if self.statment.loc[index,"activity"]:
                while((invoice["Departure"]-invoice["Arrival"]).days != 0):

                    for contract_name, contract_object in reversed(self.offers_dict.items()):
                        if (invoice["Departure"]-invoice["Arrival"]).days == 0:
                            break


                        self.contract_name = contract_name

                        if (invoice["Res_date"] >= contract_object.start_date and invoice["Res_date"] <= contract_object.end_date) or contract_name == "contract":
                            
                            # contract not active
                            if not(contract_object.activity):
                                self.statment.loc[index,"activity"] = 0
                                
                                if (self.statment.loc[index,"error_type"]):
                                    self.statment.loc[index,"error_type"] += ", "
                                self.statment.loc[index,"error_type"] += f"error in it's spo ({contract_name})"
                                
                                break
                            
                            # rate code not in contract
                            if not(invoice["Rate code"] in contract_object.contract_sheet.columns):
                                
                                self.statment.loc[index,"activity"] = 0
                                
                                if (self.statment.loc[index,"error_type"]):
                                    self.statment.loc[index,"error_type"] += ", "
                                self.statment.loc[index,"error_type"] += "error in rate code"
                                
                                break
                            
                            new_date_range,invoice, valid = self.oneContractDates(invoice,contract_object.contract_sheet,index)
                            if new_date_range[invoice["Rate code"]].isna().any() or not(valid):
                                continue

                            date_range = pd.merge(date_range,new_date_range, how='outer')
                            new_date_range = self.optimize_invoice_offers(index, invoice, contract_name, contract_object, new_date_range, False)
                            
                            contract_date_range_dict[contract_name] = new_date_range
                            

                            
                            if ((invoice["Departure"]-invoice["Arrival"]).days == 0):
                                date_range = self.optimize_invoice_offers(index, invoice, contract_name, contract_object, date_range, False)


                                new_date_range = self.optimize_invoice_offers(index, invoice, contract_name, contract_object, date_range, False)
                                #new_date_range["total price"] -= new_date_range[invoice["Rate code"]].iloc[-1]
                                #new_date_range["Nights"].iloc[-1] = new_date_range["Nights"].iloc[-1] - pd.to_timedelta(1, unit='d')
                                #new_date_range["total price"].iloc[-1] -= new_date_range["price"].iloc[-1]
                                contract_date_range_dict[contract_name] = new_date_range
                                
                                Total_price = date_range["total price"][0] 
                                #Total_price -= date_range[invoice["Rate code"]].iloc[-1]
                                Index_contract_date_range_dict[index] = contract_date_range_dict
                                
                                index_price_dict[index] = Total_price
                                continue
                    


                    if self.statment.loc[index,"activity"] != 0 and self.statment.loc[index,"error_type"] == "":
                        try:
                            index_price_dict[index] = Total_price - new_date_range[rate_code].iloc[-1]
                        except:
                            self.statment.loc[index,"error_type"] = "unexpected error"
                            break

                        new_date_range["Nights"].iloc[-1] = new_date_range["Nights"].iloc[-1] - pd.to_timedelta(1, unit='d')
                        new_date_range["total price"].iloc[-1] -= new_date_range[rate_code].iloc[-1]
                        new_date_range["price with offers"].iloc[-1] -= new_date_range[rate_code].iloc[-1]
                        new_date_range["price"].iloc[-1] -= new_date_range[rate_code].iloc[-1]

                        if not(index in index_price_dict) and self.statment.loc[index,"activity"] == 1:
                            self.statment.loc[index,"error_type"] += "reservation date not valid"
                            self.statment.loc[index,"activity"] = 0
                        break
                    else:
                        break
                

                # by arrival
                if (contract_object.sbi) and (invoice["Res_date"] >= contract_object.start_date and invoice["Res_date"] <= contract_object.end_date) and (invoice["Departure"] >= contract_object.contract_sheet["first date"][0] and invoice["Arrival"] <= contract_object.contract_sheet["second date"][-1]):
                    
                    date_range = contract_object.contract_sheet[(invoice["Arrival"] <= contract_object.contract_sheet["second date"]) & (invoice["Departure"] >= contract_object.contract_sheet["first date"])].reset_index(drop = True)
                    
                    index_price_dict[index] = (invoice["Departure"] - invoice["Arrival"]) - pd.Timedelta(days=1)
                    
                    
                if self.statment.loc[index,"activity"] == 0:
                    
                    continue
                    
        return index_price_dict, Index_contract_date_range_dict, self.statment



def get_offer_contract_data(offer_name):
    conn = sqlite3.connect('setups.db')  # Update 'setups.db' with your actual database name
    c = conn.cursor()
    
    c.execute(f"SELECT * FROM {offer_name}")
    rows = c.fetchall()
    offer_contract_data = {}
    for row in rows:
        contract_data = {}
        contract_data["contract_name"] = row[0]
        contract_data["offer_name"] = row[1]
        contract_data["offer_data"] = row[2]
        
        eb1 = {"enable": row[3], "percentage": row[4], "date": parse_date(row[5])}
        eb2 = {"enable": row[6], "percentage": row[7], "date": parse_date(row[8])}
        reduc1 = {"enable": row[9], "percentage": row[10], "column": row[11]}
        reduc2 = {"enable": row[12], "percentage": row[13], "column": row[14]}
        lt = {"enable": row[15], "percentage": row[16], "days": row[17]}
        senior = {"enable": row[18], "percentage": row[19], "column": row[20]}
        combinations = {"eb_lt": row[21], "eb_reduc": row[22], "eb_senior": row[23]}
        start_date = parse_date(row[24])
        end_date = parse_date(row[25])
        sbi = row[26]
        active = row[27]
        
        contract_data["earlyBooking1"] = eb1
        contract_data["earlyBooking2"] = eb2
        contract_data["reduction1"] = reduc1
        contract_data["reduction2"] = reduc2
        contract_data["longTerm"] = lt
        contract_data["senior"] = senior
        contract_data["combinations"] = combinations
        contract_data["start_date"] = start_date
        contract_data["end_date"] = end_date
        contract_data["active"] = active
        contract_data["sbi"] = sbi

        offer_contract_data[contract_data['contract_name']] = contract_data

    conn.close()
    return offer_contract_data




def parse_date(date_string):
    if date_string:
        # Define a list of possible date formats
        date_formats = [
            '%m/%d/%y', '%m-%d-%y', '%Y-%m-%d', '%d-%m-%Y',  # Various common formats
            '%m/%d/%Y', '%m-%d-%Y', '%d-%m-%y', '%d/%m/%y',  # More variations
            '%b %d, %Y', '%B %d, %Y',  # Month name abbreviations and full names
            '%b %d %Y', '%B %d %Y', '%b. %d, %Y', '%B. %d, %Y',  # With or without dots after month abbreviation
            '%d %b %Y', '%d %B %Y',  # Day and month swapped
            '%Y/%m/%d', '%Y-%m-%d %H:%M:%S'  # ISO format with or without time
        ]

        # Try to match the date string with the regular expressions for the defined formats
        for date_format in date_formats:
            try:
                parsed_date = pd.to_datetime(date_string, format=date_format)
                return parsed_date
            except ValueError:
                continue

        # If none of the formats matched, return None or handle the case as per your requirement
        return None
    return None







if __name__ == "__main__":
    
    # Contract
    # FileUploader
    file = FileUploader("test files/index Invo.xlsx")
    setup_name = "Biblio_Siva_Golden"
    values = get_offer_contract_data(setup_name)
    offers_dict = {} 

    for contract_name, contract_data in file.contracts_sheets.items():
        offers_dict[contract_name] = Contract(contract_name,contract_data,file.contracts_activity[contract_name],values[contract_name]["senior"],values[contract_name]["earlyBooking1"],values[contract_name]["earlyBooking2"],values[contract_name]["longTerm"],values[contract_name]["reduction1"],values[contract_name]["reduction2"],values[contract_name]["combinations"],values[contract_name]["start_date"],values[contract_name]["end_date"])

    invoice_m = Invoice(file, offers_dict).metrices
    invoice_dict = invoice_m[0]

    # Example DataFrame
    invoice_df = invoice_m[2]
    invoice_df["diff-hotel"] = 0
    # Subtraction
    for key, value in invoice_dict.items():
        invoice_df["diff-hotel"].iloc[key] = invoice_df["Amount-hotel"].iloc[key] - value

    # Printing the updated DataFrame
    print(invoice_df["diff-hotel"])


