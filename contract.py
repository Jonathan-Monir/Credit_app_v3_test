from typing import Any
import pandas as pd

class Contract:
    global_index = 0

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Initializes a Contract object with a dataframe.
        Sets the start and end dates based on the dataframe.
        Assigns a unique index to each Contract object.

        Args:
            dataframe: A dataframe containing contract data.
        """
        self.dataframe = dataframe
        self.start_date = dataframe.loc[0, "first date"]
        self.end_date = dataframe.iloc[-1]["second date"]
        self.index = Contract.global_index
        Contract.global_index += 1
