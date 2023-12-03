from contract import Contract
from file_uploader import FileUploader
import pandas as pd
import numpy as np
from collections import OrderedDict

class InvoiceMapping:
    def __init__(self, statment, Contracts):
        self.statment =  statment
        self.Contracts = Contracts
        
        self.reservation_date = statment["Res_date"]
        self.Arrival = statment["Arrival"]
        self.Departure = statment["Departure"]
        self.room_type = statment["Rate code"]
        
        self.test = np.vectorize(self.compute_days)(self.Arrival,self.Departure,self.room_type,self.reservation_date)
        self.applied_contracts = pd.DataFrame(columns=['first date', 'second date'])
    def validate_contract(self,reservation_date):
        valid_contracts = {}
        
        for key,contract in reversed(self.Contracts.items()):
            if contract.start_date <= reservation_date and contract.end_date >= reservation_date:
                valid_contracts[key] = contract

        return valid_contracts
        
    def days_prices_calc(self,Arrival,Departure,room_type,contract):
        filtered_contract = contract[(contract['second date'] > Arrival) & (contract['first date'] < Departure)]
        filtered_contract = filtered_contract.reset_index(drop=True)
        
        filtered_contract.loc[0,'first date'] = Arrival
        filtered_contract.loc[len(filtered_contract) - 1,'second date'] = Departure
        
        if self.applied_contracts.empty:
            self.applied_contracts = filtered_contract[['first date', 'second date']]
            
        else:
            self.applied_contracts = self.applied_contracts._append(filtered_contract[['first date', 'second date']])
        
        return filtered_contract
    
    def compute_days(self,Arrival,Departure,room_type,reservation_date):
        valid_contracts = self.validate_contract(reservation_date)
        self.applied_contracts = pd.DataFrame(columns=['first date', 'second date'])
        for key,Contract in valid_contracts.items():
            
            # print("key: ",key)
            # print("Arrival: ",Arrival)
            # print("Departure: ",Departure)
            self.days_prices_calc(Arrival,Departure,room_type,Contract.dataframe)
        # print(self.applied_contracts,"\n")