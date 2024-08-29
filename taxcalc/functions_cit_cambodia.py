"""
Functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit



@iterate_jit(nopython=True)
def Total_turnover(Oper_rev, Sub_rev, Other_rev, Turnover):
    """
    Compute turnover of business - sum of operating and non-operating revenues
    """
    Turnover = Oper_rev + Sub_rev + Other_rev
    return Turnover


@iterate_jit(nopython=True)
def Total_assets(assets, Total_assets):
    """
    Compute total assets of business - sum of current and non-current assets
    """
    Total_assets = assets
    return Total_assets


@iterate_jit(nopython=True)
def Sector(Sector_short, sector):
    
    """
    Determine sector of business
    
    Sector      Sector name
    1           Agriculture
    2           Service
    3           Manufacturing
    4           Mining
    5           Insurance 
    
    """
    sector = Sector_short
    return sector

@iterate_jit(nopython=True)
def Firm_size(TO_thd1, Asset_thd1, TO_thd2, Asset_thd2, TO_thd3, TO_thd4, TO_thd5, Asset_thd3, sector, Turnover, Total_assets, size):
    """
      
    Compute size of firm based on turnover and assets threshold
    
    ------------------------------------------------------------------------------------
    Sector        L                                        M
              TO        Assets                  TO                       Assets
    ------------------------------------------------------------------------------------
    Agri    >T1 (4bn)    >A1 (2bn)   T2 (1bn) < TO <= T1 (4bn)    A2 (1bn) < A <= A1 (2bn)   
    Service >T3 (6bn)    >A1 (2bn)   T2 (1bn) < TO <= T3 (6bn)    A2 (1bn) < A <= A1 (2bn)
    Manuf   >T4 (8bn)    >A3 (4bn)   T5 (1.6bn) < TO <= T4 (8bn)  A1 (2bn) < A <= A3 (4bn)
    
    """
    (T1, A1, T2, A2, T3, T4, T5, A3)  = (TO_thd1, Asset_thd1, TO_thd2, Asset_thd2, TO_thd3, TO_thd4, TO_thd5, Asset_thd3)
    if sector == 1:
        if Turnover > T1 or Total_assets > A1:
            size = 2
        elif (Turnover > T2 and Turnover <= T1) or (Total_assets > A2 and Total_assets <= A1):
            size = 1
        else:
            size = 0
    elif sector == 2 or sector == 5:
        if Turnover > T3 or Total_assets > A1:
            size = 2
        elif (Turnover > T2 and Turnover <= T3) or (Total_assets > A2 and Total_assets <= A1):
            size = 1
        else:
            size = 0
    elif sector == 3 or sector == 4:
        if Turnover > T4 or Total_assets > A3:
            size = 2
        elif (Turnover > T5 and Turnover <= T4) or (Total_assets > A1 and Total_assets <= A3):
            size = 1
        else:
            size = 0
    return size

# @iterate_jit(nopython=True)
# def Firm_size(Legal_form, size):
#     if Legal_form == "Sole Prop Ltd":
#         size="S"
#     else:
#         size="L"
#     return size
    
'''
-------------------------------------------------------------------------------------
Calculation of Depreciation Allowance 
-------------------------------------------------------------------------------------
'''


@iterate_jit(nopython=True)
def Normal_depr_base(Op_wdv, Add_assets, Dispose_assets, normal_depr_base):
    """
    Return the depreciation base
    """
    normal_depr_base = Op_wdv + Add_assets - Dispose_assets
    return normal_depr_base


@iterate_jit(nopython=True)
def Normal_depr(normal_depr_base, depr, depr_rate, normal_depr):
    """
    Return the depreciation for each asset class.
    """
    normal_depr = max(normal_depr_base * depr_rate, depr)
    return normal_depr

'''
-------------------------------------------------------------------------------------
Calculation of Special depreciation
-------------------------------------------------------------------------------------
'''


@iterate_jit(nopython=True)
def Spl_depr_base(Add_assets_spl, spl_depr_base):
    """
    Return the special depreciation base
    """
    spl_depr_base = Add_assets_spl
    return spl_depr_base

@iterate_jit(nopython=True)
def Spl_depr(spl_depr_rate, Spl_depr_flag, spl_depr_base, spl_depr):
    """
    Return the special depreciation
    """
    if Spl_depr_flag == 1:
        spl_depr = spl_depr_base * spl_depr_rate
    else:
        spl_depr = 0
    return spl_depr


'''
-------------------------------------------------------------------------------------
Calculation of Closing WDV
-------------------------------------------------------------------------------------
'''


@iterate_jit(nopython=True)
def Total_depr(normal_depr, spl_depr, total_depr):
    """
    Return the total depreciation - sum of normal and special depreciation.
    """
    total_depr = normal_depr + spl_depr
    return total_depr


@iterate_jit(nopython=True)
def Cl_WDV(normal_depr_base, spl_depr_base, total_depr, Cl_wdv):
    """
    Return the closing written down value of depreciation base
    """
    Cl_wdv = normal_depr_base + spl_depr_base - total_depr
    return Cl_wdv


'''
-------------------------------------------------------------------------------------
Calculation of profit chargeable to tax
-------------------------------------------------------------------------------------
'''


@iterate_jit(nopython=True)
def Net_accounting_profit(profit_before_tax, net_accounting_profit):
    """
    Compute accounting profit from business
    """
    net_accounting_profit = profit_before_tax
    return net_accounting_profit


@iterate_jit(nopython=True)
def Total_additions(Donations_grants, non_ded_exp, unrecorded_inc, total_additions):
    """
    Compute additions to accounting profit from business
    """
    total_additions = Donations_grants + non_ded_exp + unrecorded_inc
    return total_additions


@iterate_jit(nopython=True)
def Total_deductions(total_depr, dec_provision, loss_disposal, other_ded_exp, total_deductions):
    """
    Compute deductions from accountinf profit
    """
    total_deductions = total_depr + dec_provision + loss_disposal + other_ded_exp
    return total_deductions


@iterate_jit(nopython=True)
def Total_non_tax_inc(dividends, capgain_disp_assets, other_inc, total_non_tax_inc):
    """
    Compute total taxable profits afer adding back non-allowable deductions.
    """
    total_non_tax_inc = dividends + capgain_disp_assets + other_inc
    return total_non_tax_inc


'''
-------------------------------------------------------------------------------------
Calculation of adjusted profits
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def Adj_profit(net_accounting_profit, total_additions, total_deductions, total_non_tax_inc, rent_inc, adjusted_profit ):
    """
    Compute total taxable profits afer adding back non-allowable deductions.
    """
    adjusted_profit = net_accounting_profit + total_additions + rent_inc - total_deductions - total_non_tax_inc
    return adjusted_profit


'''
-------------------------------------------------------------------------------------
Calculation of allowable charity contributions
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def Allowed_charity(adjusted_profit, charity_cont, rate_ded_charity, ded_charity, non_ded_charity):
    """
    Compute allowable charitable expenses
    """
    max_ded_charity = rate_ded_charity * (adjusted_profit + charity_cont)
    ded_charity = min(max_ded_charity, charity_cont)
    non_ded_charity = charity_cont - ded_charity
    return (ded_charity, non_ded_charity)


'''
-------------------------------------------------------------------------------------
Calculation of profit before interest deduction
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def Profit_before_int(adjusted_profit, non_ded_charity, profit_before_int):
    """
    Compute total taxable profits before interest is allowed as deduction.
    """
    profit_before_int = adjusted_profit + non_ded_charity
    return profit_before_int

'''
-------------------------------------------------------------------------------------
Calculation of allowable interest deduction
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def Allowed_interest(profit_before_int, int_exp, int_inc, rate_int_ded, non_ded_int):
    """
    Compute allowable interest deduction
    """
    net_non_int_inc = max(profit_before_int + int_exp - int_inc, 0)
    max_ded_int = rate_int_ded * net_non_int_inc + int_inc
    if int_exp > max_ded_int:
        non_ded_int = int_exp - max_ded_int
    else:
        non_ded_int = 0.
    return non_ded_int


'''
-------------------------------------------------------------------------------------
Calculation of profit after interest deduction
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def Profit_after_int(profit_before_int, non_ded_int, profit_after_int):
    """
    Compute total taxable profits afer allowable interest deduction.
    """
    profit_after_int = profit_before_int + non_ded_int
    return profit_after_int

'''
-------------------------------------------------------------------------------------
Calculation of net profit
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def Taxable_profit_after_adjloss(profit_after_int, loss_cf_limit, Loss_lag1, 
                                  Loss_lag2, Loss_lag3, Loss_lag4, Loss_lag5, 
                                  Loss_lag6, Loss_lag7, Loss_lag8, Loss_lag9, 
                                  Loss_lag10, newloss1, newloss2, newloss3, 
                                  newloss4, newloss5, newloss6, newloss7,
                                  newloss8, newloss9, newloss10, 
                                  Used_loss_total, net_taxable_profit):
    
    """
    Compute net tax base afer allowing brought forward losses.
    """
    BF_loss = np.array([Loss_lag1, Loss_lag2, Loss_lag3, Loss_lag4, Loss_lag5, Loss_lag6,
                        Loss_lag7, Loss_lag8, Loss_lag9, Loss_lag10])
    #print('BF Loss is', BF_loss)
    N = int(loss_cf_limit)
    Used_loss = np.zeros(N)
    
    if N == 0:
        (newloss1, newloss2, newloss3, newloss4, newloss5,
          newloss6, newloss7, newloss8, newloss9, newloss10) = np.zeros(10)
        net_taxable_profit = profit_after_int
        Used_loss_total = Used_loss.sum()
    else:
        BF_loss = BF_loss[:N]
                
        if profit_after_int < 0:
            CYL = abs(profit_after_int)
                    
        elif profit_after_int >= 0:
            CYL = 0
            Cum_used_loss = 0
            for i in range(N, 0, -1):
                GTI = profit_after_int - Cum_used_loss
                Used_loss[i-1] = min(BF_loss[i-1], GTI)
                Cum_used_loss += Used_loss[i-1]
            # for i in range(N):
            #     GTI = profit_after_int - Cum_used_loss
            #     Used_loss[i] = min(BF_loss[i], GTI)
            #     Cum_used_loss += Used_loss[i]
        
        New_loss = BF_loss - Used_loss
        Used_loss_total = Used_loss.sum()
        net_taxable_profit = profit_after_int - Used_loss_total
        newloss1 = CYL
        (newloss2, newloss3, newloss4, newloss5,
         newloss6, newloss7, newloss8, newloss9, newloss10) = np.append(New_loss[:-1], np.zeros(10-N))

    return (net_taxable_profit, newloss1, newloss2, newloss3, newloss4, newloss5, 
            newloss6, newloss7, newloss8, newloss9, newloss10, Used_loss_total)



@iterate_jit(nopython=True)
def Net_tax_base_behavior(cit_rate_std, cit_rate_std_curr_law, cit_rate_mining, cit_rate_mining_curr_law, 
                          cit_rate_insurance, cit_rate_insurance_curr_law, cit_rate_qip, cit_rate_qip_curr_law, 
                          sector, Legal_form, elasticity_cit_taxable_income_threshold, elasticity_cit_taxable_income_value, 
                          QIP_flag, net_taxable_profit, net_tax_base_behavior):
    """
    Compute net taxable profits afer allowing behavioral adjustments based on elasticity
    """
    NP = max(net_taxable_profit, 0)
    elasticity_taxable_income_threshold0 = elasticity_cit_taxable_income_threshold[0]
    elasticity_taxable_income_threshold1 = elasticity_cit_taxable_income_threshold[1]
    #elasticity_taxable_income_threshold2 = elasticity_cit_taxable_income_threshold[2]
    elasticity_taxable_income_value0=elasticity_cit_taxable_income_value[0]
    elasticity_taxable_income_value1=elasticity_cit_taxable_income_value[1]
    elasticity_taxable_income_value2=elasticity_cit_taxable_income_value[2]
    if NP<=0:
        elasticity=0
    elif NP>0 and NP<=elasticity_taxable_income_threshold0:
        elasticity=elasticity_taxable_income_value0
    elif NP>elasticity_taxable_income_threshold0 and NP<=elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value1
    elif NP>elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value2
    
    
    frac_change_net_of_cit_rate_std = ((1-cit_rate_std)-(1-cit_rate_std_curr_law))/(1-cit_rate_std_curr_law) 
    frac_change_net_of_cit_rate_mining = ((1-cit_rate_mining)-(1-cit_rate_mining_curr_law))/(1-cit_rate_mining_curr_law)
    frac_change_net_of_cit_rate_insurance = ((1-cit_rate_insurance)-(1-cit_rate_insurance_curr_law))/(1-cit_rate_insurance_curr_law)
    frac_change_net_of_cit_rate_qip = ((1-cit_rate_qip)-(1-cit_rate_qip_curr_law))/(1-cit_rate_qip_curr_law)
    
    # if (sector == 3 or sector == 2) and (size != 0):
    if (sector == 1 or sector == 2 or sector == 3) and Legal_form != 1:
        frac_change_Net_tax_base = elasticity*(frac_change_net_of_cit_rate_std)
    elif sector == 4:
        frac_change_Net_tax_base = elasticity*(frac_change_net_of_cit_rate_mining)
    elif sector == 5:
        frac_change_Net_tax_base = elasticity*(frac_change_net_of_cit_rate_insurance)
    elif QIP_flag == 1:
        frac_change_Net_tax_base = elasticity*(frac_change_net_of_cit_rate_qip)
    else:
        frac_change_Net_tax_base = 0
        
    net_tax_base_behavior = NP*(1+frac_change_Net_tax_base) 
    return net_tax_base_behavior



'''
-------------------------------------------------------------------------------------
Calculation of excess tax
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def Excess_tax(net_tax_base_behavior, accum_inc, accum_exp, prop_accum1, prop_accum2, prop_accum3,
               etax_rate1, etax_rate2, etax_rate3, excess_tax):
    """
    Compute total excess tax in case of mining companies.
    """
    if accum_exp == 0: 
        prop_accum = 0
    else:
        prop_accum = accum_inc / accum_exp
    if (prop_accum <= prop_accum1) or (prop_accum == 0):
        excess_tax = 0 
    elif (prop_accum > prop_accum1) and (prop_accum <= prop_accum2):
        excess_tax = etax_rate1 * net_tax_base_behavior * (prop_accum - prop_accum1)/prop_accum
    elif (prop_accum > prop_accum2) and (prop_accum <= prop_accum3 ):
        excess_tax = etax_rate2 * net_tax_base_behavior * (prop_accum - prop_accum2)/prop_accum + \
                     etax_rate1 * net_tax_base_behavior * (prop_accum2 - prop_accum1)/prop_accum2
    elif (prop_accum > prop_accum3):
        excess_tax = etax_rate3 * net_tax_base_behavior * (prop_accum - prop_accum3)/prop_accum + \
                     etax_rate2 * net_tax_base_behavior * (prop_accum3 - prop_accum2)/prop_accum3 + \
                     etax_rate1 * net_tax_base_behavior * (prop_accum2 - prop_accum1)/prop_accum2
    else:
        excess_tax = 0
    return excess_tax

'''
-------------------------------------------------------------------------------------
Calculation of corprate tax
-------------------------------------------------------------------------------------
'''

@iterate_jit(nopython=True)
def cit_liability(net_tax_base_behavior, excess_tax, sector, size, Legal_form, QIP_flag, mintax_flag, Turnover, 
                  cit_rate_std, cit_rate_mining, switch_prog, cit_rate_insurance, cit_rate_qip, cit_rate1, 
                  cit_rate2, cit_rate3, cit_rate4, cit_rate5, tbrk1, tbrk2, tbrk3, tbrk4, mintax_rate, citax):
    """
    Compute tax liability given the corporate rate
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    if net_tax_base_behavior <= 0:
        citax = 0
    else:
        if (Legal_form == 1):
           citax = ((cit_rate1 * min(net_tax_base_behavior, tbrk1) + 
                    cit_rate2 * min(tbrk2 - tbrk1, max(0., net_tax_base_behavior - tbrk1)) +
                    cit_rate3 * min(tbrk3 - tbrk2, max(0., net_tax_base_behavior - tbrk2)) +
                    cit_rate4 * min(tbrk4 - tbrk3, max(0., net_tax_base_behavior - tbrk3)) +
                    cit_rate5 * max(0., net_tax_base_behavior - tbrk4)))*(switch_prog) + net_tax_base_behavior*cit_rate_std*(1-switch_prog)
        elif sector == 4:
            citax = cit_rate_mining * max(net_tax_base_behavior, 0) + excess_tax
        elif sector == 5:
            citax = cit_rate_insurance * max(net_tax_base_behavior, 0)
        elif QIP_flag == 1:
            citax = cit_rate_qip * max(net_tax_base_behavior, 0)
        else:
            citax = cit_rate_std * max(net_tax_base_behavior, 0)
        
    return citax






# mintax = max(Turnover, 0) * mintax_rate

# if mintax_flag == 1:
#     #citax = max(citax, mintax)
#     citax = citax
# else:
#     citax = max(citax, MAT)
#     #citax = citax


