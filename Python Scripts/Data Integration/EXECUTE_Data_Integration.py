#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Samiha Binte Shahid
Email: sbint003@ucr.edu
Github: @SamihaShahid

"""
import pandas as pd
import numpy as np

from DataInt_mainFunc import *
from Merge_MultLumpCom import *
from Get_LumpCom_Spec import *
from utils import import_fc_dataset, sort_nmog, assign_study_column, str_float
from connect_with_mysql import*
output_db=connect_db('neiva_output_db')

'''
This script integrates primary database tables into a unified dataset. 
The functions employed in this integration
process are sourced from DataInt_mainFunc.py, Merge_MultLumpCom.py,
Get_LumpCom_Spec.py, and utils.py scripts. 
The final, integrated dataset is saved as IntData in the output_db.
'''

# Integrates the primary database datasets.
int_df=DataInt()

# Extracts dataframe where pollutant_category is NMOC_g 
nmogdf=Get_nmog(int_df)   

# Processes and manages record with multiple lumped compounds.
r_iddf, iddf =reduce_multiple_LumCom(nmogdf)

# Updates nmogdf by replacing iddf with r_iddf
nmogdf=insert_rdf_nmogdf(nmogdf,r_iddf,iddf) 

# Assigns study column to nmogdf
nmogdf=assign_study_column(nmogdf)

# Decomposes lumped compounds and aligns with individual compounds
lc_spec_df=Get_LumCom_Spec(nmogdf)

# Sorts nmogdf for further processing
nmogdf=sort_nmog(nmogdf)

# Loads the dataset for fractional contribution calculations to the backend database
import_fc_dataset(nmogdf,lc_spec_df)

# Sorts and merges inorganic gases, particulate matter data with nmogdf
igdf=sort_igdf(int_df)
pmdf=sort_pmdf(int_df)
mdf=igdf.append(nmogdf).append(pmdf)

# Storing the final integrated dataset in the database 
mdf=mdf.reset_index(drop=True)

# Adjusts datatype for the 'mm' column
mdf=str_float(mdf,'mm')

mdf.to_sql(name='IntData',con=output_db, if_exists='replace', index=False)
print('Updated the Integrated dataset in NEIAV_db.sql')



