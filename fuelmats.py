import sys
from openpyxl import load_workbook
import pandas as pd

def main():
    fuel_wb_name = "Core Burnup History 20201117.xlsx"
    burnup_sht_name = "Core History"
    if fuel_wb_name is None: fuel_wb_name = input("Input the fuel burnup spreadsheet name, with file extension: ")

    # burnup_sht: pandas dataframe
    burnup_df = pd.read_excel(fuel_wb_name, sheet_name=burnup_sht_name, usecols='I,V:X')

    # Currently, 'burnup_sht' uses the first row as column names. Rename it to the column letters used in the XLSX.
    burnup_df.columns = ['I','V','W','X']

    # Let's get rid of all the empty rows or rows with text in them.
    burnup_df = burnup_df[pd.to_numeric(burnup_df.iloc[:, 0], errors='coerce').notnull()]

    # Let's get rid of FE 101, as that is not a regular FE used in our MCNP code.
    burnup_df.drop(burnup_df.loc[burnup_df['I'] == 101].index, inplace=True)
    burnup_df.reset_index(drop=True, inplace=True)

    """ 
    df.apply(func, axis= {0 or ‘index’, 1 or ‘columns’, default 0}, result_type={‘expand’, default None}
    
    Notice that the get_mass_frac function actually outputs a list of 1 int and 5 floats.
    With result_type = None, the list is one entry in the new mass_fracs_df.
    With result_type = 'expand', each element of the list is separated into different columns
    """
    mass_fracs_df = burnup_df.apply(get_mass_fracs, axis=1, result_type='expand')

    # Rename columns to their respective variable names
    mass_fracs_df.columns = ['fe_id', 'g_U235', 'g_U238', 'g_Pu239', 'g_Zr', 'g_H']

    # Change fe_id values to integer, if they aren't already
    mass_fracs_df.astype({'fe_id':'int8'})

    # 'df.iloc[:,n]' prints the (n+1)th column of the dataframe

    for i in range(0,len(mass_fracs_df)):
        print(f"m{int(mass_fracs_df.loc[i,'fe_id'])}    ")
    #print(burnup_df)
    #print(len(mass_fracs_df))
    '''
    for fe_id in burnup_sht.iloc[:, 0]:
        if type(fe_id)=="int":
            print(burnup_sht.iloc[])
            
            g_Pu239 = V
            g_U235 = X
            g_U238 = W-X
            g_U_total = g_Pu239 + g_U235 + g_U238 # should be <= 8.5% of total weight (mass) of FE
            g_ZrH_total = g_U_total/8.5*91.5
            g_Zr = 1/(1.575+1)*g_ZrH_total
            g_H = 1.575/(1.575+1)*g_ZrH_total
    '''
# Adapted from: https://stackoverflow.com/questions/27575854/vectorizing-a-function-in-pandas
def get_mass_fracs(row):
    fe_id = int(round(row["I"]))
    g_Pu239 = row["V"]
    g_U235 = row["X"]
    g_U = row["W"]
    g_U238 = g_U - g_U235
    g_U_total = g_Pu239 + g_U235 + g_U238  # should be <= 8.5% of total weight (mass) of FE
    g_ZrH_total = g_U_total / 8.5 * 91.5
    g_Zr = 1 / (1.575 + 1) * g_ZrH_total
    g_H = 1.575 / (1.575 + 1) * g_ZrH_total
    return fe_id, g_U235, g_U238, g_Pu239, g_Zr, g_H


if __name__ == "__main__":
    main()
