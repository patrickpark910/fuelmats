import sys
import pandas as pd
from openpyxl import load_workbook

def main():
    fuel_wb_name = "Core Burnup History 20201117.xlsx"
    burnup_sht_name = "Core History"

    # pd.read_excel({file_name}, sheet_name= , usecols= )
    burnup_df = pd.read_excel(fuel_wb_name, sheet_name=burnup_sht_name, usecols='I,V:X', engine='openpyxl')

    # Currently, `burnup_sht' uses the first row as column names. Rename it to the column column letters used in XLSX.
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
    mass_fracs_df.columns = ['fe_id', 'g_U235', 'g_U238', 'g_Pu239', 'g_Zr', 'g_H',
                             'a_U235', 'a_U238', 'a_Pu239', 'a_Zr', 'a_H']

    results_file = open('results.txt', 'w')

    for i in range(0,len(mass_fracs_df)):
        results_file.write(f"c\n"
              f"m{int(mass_fracs_df.loc[i,'fe_id'])}    92235.80c {'{:.6e}'.format(mass_fracs_df.loc[i,'a_U235'])} $ {round(mass_fracs_df.loc[i,'g_U235'],6):.6f} g\n"
              f"         92238.80c {'{:.6e}'.format(mass_fracs_df.loc[i,'a_U238'])} $ {round(mass_fracs_df.loc[i,'g_U238'],6):.6f} g\n"
              f"         94239.80c {'{:.6e}'.format(mass_fracs_df.loc[i,'a_Pu239'])} $ {round(mass_fracs_df.loc[i,'g_Pu239'],6):.6f} g\n"
              f"         40000.66c {'{:.6e}'.format(mass_fracs_df.loc[i,'a_Zr'])} $ {round(mass_fracs_df.loc[i,'g_Zr'],6):.6f} g\n"
              f"          1001.80c {'{:.6e}'.format(mass_fracs_df.loc[i,'a_H'])} $ {round(mass_fracs_df.loc[i,'g_H'],6):.6f} g\n"
              f"mt{int(mass_fracs_df.loc[i,'fe_id'])} h/zr.10t zr/h.10t\n"
              f"c\n")

    results_file.close()

    # print(mass_fracs_df)
"""
m{mass_fracs_df.loc[i, 'fe_id']}    92235.80c {a_U235} $ {g_U235} g\n
         92238.80c 4.013011e+23 $ 158.635084 g
         94239.80c 1.017415e+21 $ 0.403878 g
         40000.66c 1.359118e+25 $ 2058.854372 g
          1001.80c 2.140611e+25 $ 35.828758 g
"""

def get_mass_fracs(row):
    AMU_U235 = 235.0439299
    AMU_U238 = 238.05078826
    AMU_PU239 = 239.0521634
    AMU_ZR = 91.224
    AMU_H = 1.00794
    AVO = 6.022e23
    RATIO_HZR = 1.575 # TS allows 1.55 to 1.60. This is an ATOM ratio
    fe_id = row['I']
    g_Pu239 = row['V']
    g_U = row['W']
    g_U235 = row['X']
    g_U238 = g_U - g_U235 # We assume all the U is either U-235 or U-238.
    g_U_total = g_Pu239 + g_U235 + g_U238 # should be <= 8.5% of total weight (mass) of FE
    g_ZrH_total = g_U_total/ 8.5 * 91.5 # Assume rest of FE mass of ZrH
    a_Pu239 = g_Pu239 / AMU_PU239 * AVO
    a_U235 = g_U235 / AMU_U235 * AVO
    a_U238 = g_U238 / AMU_U238 * AVO
    a_Zr = g_ZrH_total/(AMU_ZR/AVO + RATIO_HZR*AMU_H/AVO)
    a_H = RATIO_HZR * a_Zr
    g_Zr = a_Zr * AMU_ZR / AVO
    g_H = a_H * AMU_H / AVO

    return fe_id, g_U235, g_U238, g_Pu239, g_Zr, g_H, a_U235, a_U238, a_Pu239, a_Zr, a_H
    # This process is known as 'vectorization'





if __name__ == "__main__": main()