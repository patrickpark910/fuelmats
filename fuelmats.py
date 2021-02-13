import sys
from openpyxl import load_workbook
import pandas as pd

def main():
    fuel_wb_name = "Core Burnup History 20201117.xlsx"
    burnup_sht_name = "Core History"
    if fuel_wb_name is None: fuel_wb_name = input("Input the fuel burnup spreadsheet name, with file extension: ")

    burnup_sht = pd.read_excel(fuel_wb_name, sheet_name=burnup_sht_name, usecols='I:X')
    # burnup_sht: pandas dataframe
    # 'df.iloc[:,n]' prints the (n+1)th column of the dataframe
    for fe_id in burnup_sht.iloc[:, 0]:
        if type(fe_id)=="int":

            g_Pu239 = V
            g_U235 = X
            g_U238 = W-X
            g_U_total = g_Pu239 + g_U235 + g_U238 # should be <= 8.5% of total weight (mass) of FE
            g_ZrH_total = g_U_total/8.5*91.5
            g_Zr = 1/(1.575+1)*g_ZrH_total
            g_H = 1.575/(1.575+1)*g_ZrH_total




        # Some of the cells will be numbers (int) or words (str) or empty (nan). We just want the actual FE ID numbers.


if __name__ == "__main__":
    main()
