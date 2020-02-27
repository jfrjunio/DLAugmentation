import numpy as np
import math
import cPickle as pickle
import random
import argparse
import entropy_analysis
from copy import copy

import re

def checkIfIsICDCode(CODE):
	if CODE[0].isalpha():
		try:
			int(CODE[1:])
			return True
		except:
			return False
	else:
		return False

def generateDataAugmentation(train_all_subjectsListOfCODEsList_LIST, hprefixToCodes_Map, horiginalIDCODEToProcessCODE, actionOrderedIndexesMAP, reverse_ordered_internalCodesMap):
	
	new_all_subjectsListOfCODEsList_LIST = []	
	for subject_list_of_CODEs_List in train_all_subjectsListOfCODEsList_LIST:
		# adding the original item
		new_all_subjectsListOfCODEsList_LIST.append(subject_list_of_CODEs_List)
				
		new_subjectsListOfCODEsList_LIST = []
		for CODEs_List in subject_list_of_CODEs_List:
							
			new_CODEs_List = []			
			for item_CODE in CODEs_List:
				# Get the reverse of the mapcode
				CODE = reverse_ordered_internalCodesMap[item_CODE]
				# Only check codes that are ICD-10
				if CODE in horiginalIDCODEToProcessCODE:
					if len(list(horiginalIDCODEToProcessCODE[CODE]))>1:
						print('oi')
					item_tuple = list(horiginalIDCODEToProcessCODE[CODE])[0]	# obtiene el primer elemento
					prefix     = item_tuple[0]				

					# If the prefix appears on dataset
					if prefix in hprefixToCodes_Map and len(hprefixToCodes_Map[prefix])>0:
						# Get codes availables
						ICD10CodesAvailables = list(hprefixToCodes_Map[prefix])						
						# Pick a random code
						newidx               = random.randint(0, len(ICD10CodesAvailables) - 1)
						newCodeICD10         = 'DIAGC'+prefix+str(ICD10CodesAvailables[newidx]).strip()						
						newCodeOrdered       = actionOrderedIndexesMAP[newCodeICD10]
						new_CODEs_List.append(newCodeOrdered)
			
			if len(new_CODEs_List) > 0: # Check that have at least one code
				new_subjectsListOfCODEsList_LIST.append(new_CODEs_List)
				
		if len(new_subjectsListOfCODEsList_LIST) > 1: # Check that have at least two admissions
			new_all_subjectsListOfCODEsList_LIST.append(new_subjectsListOfCODEsList_LIST)
	
	return new_all_subjectsListOfCODEsList_LIST


def makeDataAugmentation(train_all_subjectsListOfCODEsList_LIST, actionOrderedIndexesMAP, reverse_ordered_internalCodesMap):
	prefix_ICD                   = 'DIAGC'
	hprefixToCodes_Map           = {}
	horiginalIDCODEToProcessCODE = {}
	for subject_list_of_CODEs_List in train_all_subjectsListOfCODEsList_LIST:		
		for CODEs_List in subject_list_of_CODEs_List:			
			for item_CODE in CODEs_List:				
				CODE = reverse_ordered_internalCodesMap[item_CODE]				
				if re.match("^[a-zA-Z0-9_]*$", CODE):					
					prefix_code = CODE[:5]					
					if prefix_code == prefix_ICD:  # All ICD-10 codes in INCOR dataset has as general prefix DIAGC
						# Get ICD10 code						
						icd_10_code = CODE[5:].strip()						
						# Check if is ICDCode						
						isICD10 = checkIfIsICDCode(icd_10_code)
						idx = 3
						# An example
						# CodeICD10 = I45.56
						# prefix_icd = I45
						# postfix_icd = 56
						if isICD10 and len(icd_10_code) > 3:
							# Save the prefix of codes
							prefix_icd_10_code  = icd_10_code[:idx].strip()
							# Save the postfix of codes
							postfix_icd_10_code = icd_10_code[idx:].strip()
								
							# Save in dictionary using prefix_icd_10 as key
							if prefix_icd_10_code in hprefixToCodes_Map:
								hprefixToCodes_Map[prefix_icd_10_code].add(postfix_icd_10_code)
							else:
								hprefixToCodes_Map[prefix_icd_10_code] = set()
								hprefixToCodes_Map[prefix_icd_10_code].add(postfix_icd_10_code)
							
							# save the ICD-10 codes  by separating prefix and postfix
							if CODE in horiginalIDCODEToProcessCODE:				
								horiginalIDCODEToProcessCODE[CODE].add((prefix_icd_10_code, postfix_icd_10_code))
							else:
								horiginalIDCODEToProcessCODE[CODE] = set()
								horiginalIDCODEToProcessCODE[CODE].add((prefix_icd_10_code, postfix_icd_10_code))				
			
																										
	new_train_subjectsListOfCODEsList_LIST = generateDataAugmentation(train_all_subjectsListOfCODEsList_LIST, hprefixToCodes_Map, horiginalIDCODEToProcessCODE, actionOrderedIndexesMAP, reverse_ordered_internalCodesMap)

	# Adding the other method	
	onlyTwoAdmissionsPatients = []
	for patient_admissions in new_train_subjectsListOfCODEsList_LIST:
		nAdms = len(patient_admissions)
		ithAdm = 0
		while (ithAdm < (nAdms - 1)):
			twoAdmis = []
			twoAdmis.append(patient_admissions[ithAdm])
			twoAdmis.append(patient_admissions[ithAdm + 1])
			ithAdm += 1
			onlyTwoAdmissionsPatients.append(twoAdmis)
	
	train_all_subjectsListOfCODEsList_LIST = train_all_subjectsListOfCODEsList_LIST + onlyTwoAdmissionsPatients
	
	return train_all_subjectsListOfCODEsList_LIST