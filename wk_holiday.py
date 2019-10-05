import numpy as np 
import pandas as pd
import math
import warnings
import datetime
import calendar
from pandas import Series, Timestamp
from datetime import date
import workalendar.america as wk_am
import workalendar.asia as wk_as
import workalendar.africa as wk_af
import workalendar.oceania as wk_oc
import workalendar.europe as wk_eu


#includes all holidays supported by https://github.com/peopledoc/workalendar except for China and US
class WkHoliday():
    #theoretical start end date for workalendar are absurdly wide in range,
    #so just used start end dates from rest of program
    start_date = Timestamp("1983-01-01")
    end_date = np.maximum(start_date, Timestamp("2030-01-1"))
    allowed_countries = { 
        #country names must be uppercase to access countries
        'Algeria' : wk_af.Algeria, 'Angola': wk_af.Angola, 'Benin': wk_af.Benin, 
        'Ivory Coast': wk_af.IvoryCoast, 'Madagascar': wk_af.Madagascar, 'Sao Tome': wk_af.SaoTomeAndPrincipe,
        'South Africa': wk_af.SouthAfrica, 'Barbados': wk_am.Barbados, 'Brazil': wk_am.Brazil, 
        'Canada': wk_am.Canada, 'Chile': wk_am.Chile, 'Colombia': wk_am.Colombia,
        'Mexico': wk_am.Mexico, 'Panama':wk_am.Panama, 'Paraguay': wk_am.Paraguay, 
        'Hong Kong': wk_as.HongKong, 'Israel': wk_as.Israel, 'Japan': wk_as.Japan, 
        'Malaysia': wk_as.Malaysia, 'Qatar': wk_as.Qatar, 'Singapore':wk_as.Singapore, 
        'South Korea': wk_as.SouthKorea, 'Taiwan': wk_as.Taiwan, 'Austria': wk_eu.Austria, 
        'Belgium': wk_eu.Belgium, 'Bulgaria': wk_eu.Bulgaria, 'Cayman Islands': wk_eu.CaymanIslands,
        'Croatia': wk_eu.Croatia, 'Cyprus': wk_eu.Cyprus, 'Czech Republic': wk_eu.CzechRepublic,
        'Denmark': wk_eu.Denmark, 'Estonia': wk_eu.Estonia, 'European Central Bank': wk_eu.EuropeanCentralBank,
        'Finland': wk_eu.Finland, 'France': wk_eu.France, 'Germany': wk_eu.Germany, 
        'Greece': wk_eu.Greece, 'Hungary': wk_eu.Hungary, 'Iceland': wk_eu.Iceland,
        'Ireland': wk_eu.Ireland, 'Italy': wk_eu.Italy, 'Latvia': wk_eu.Latvia,
        'Lithuania': wk_eu.Lithuania, 'Luxembourg': wk_eu.Luxembourg, 'Malta': wk_eu.Malta,
        'Netherlands': wk_eu.Netherlands, 'Norway': wk_eu.Norway, 'Poland': wk_eu.Poland,
        'Portugal': wk_eu.Portugal, 'Romania': wk_eu.Romania, 'Russia': wk_eu.Russia,
        'Slovakia': wk_eu.Slovakia, 'Slovenia': wk_eu.Slovenia, 'Spain': wk_eu.Spain,
        'Sweden': wk_eu.Sweden, 'Switzerland': wk_eu.Switzerland, 'Turkey': wk_eu.Turkey,
        'United Kingdom': wk_eu.UnitedKingdom, 'Australia': wk_oc.Australia, 'Marshall Islands': wk_oc.MarshallIslands,
        'New Zealand': wk_oc.NewZealand                   
    }

    def __init__(self, country = "Chile"):
        if country in self.allowed_countries:
            self.country = country
            self.wk_cal = self.allowed_countries.get(country)()
        else:
            raise Exception("Unsupported Country")
        self.names_list = list()
        self.dates_list = list()
        self.holidays_df = pd.DataFrame({'names': []})
        self.holidays_list = pd.Series()

    def holidays(self, start=None, end=None, return_name = False):
        if start is None:
            start = WkHoliday.start_date
        
        if end is None:
            end = WkHoliday.end_date
        start = Timestamp(start)
        end = Timestamp(end)
        start_year = start.year
        end_year = end.year
        #iterate over the years provided to compose holidays into a DataFrame, append to holiday_list
        for years in range(start_year, end_year + 1):
            #parses wk_cal twice for names and dates from tuples given from self.wk_cal.holidays(years) 
            new_df = pd.DataFrame({'names': [name[1] for name in self.wk_cal.holidays(years)]}, 
                        index = [pd.to_datetime(holiday[0]) for holiday in self.wk_cal.holidays(years)])
            for date in list(new_df.index.values):
                if (date < start) or (date > end):
                    new_df = new_df.drop(index = date)
            self.holidays_df = self.holidays_df.append(new_df)  
        self.holiday_list = pd.Series(list(self.holidays_df['names']), index = list(self.holidays_df.index.values))
        if return_name:
            return self.holiday_list
        else:
            return self.holiday_list.index
