import math
import sys
import cPickle as pickle
import random

def generateDataAugmentation(proportion, train_all_subjectsListOfCODEsList_LIST, CCS_ordered_internalCodesMap, reverse_CCS_ordered_internalCodesMap, localDiagnosisCCSToICD9, originalDiagnosisICD9_Codes):
	icd9TOCCS_Map = pickle.load(open(sys.path[0]+'/icd9_to_css_dictionary','rb'))
		
	new_train_subjectsListOfCODEsList_LIST = []	
	for idx_patient, subject_list_of_CODEs_List in enumerate(train_all_subjectsListOfCODEsList_LIST):
		# adding the original item
		new_train_subjectsListOfCODEsList_LIST.append(subject_list_of_CODEs_List)
					
		for i in range(proportion):
			new_subjectsListOfCODEsList_LIST = []
			for CODEs_List in subject_list_of_CODEs_List:
				new_CODEs_List = []			
				for CODE in CODEs_List:
					OriginalCODE = reverse_CCS_ordered_internalCodesMap[CODE]					
					newCode      = originalDiagnosisICD9_Codes[OriginalCODE]

					while (len(newCode) < 6): newCode += ' '  #pad right white spaces because the CCS mapping uses this pattern					
					codeCCS               = ('D' + icd9TOCCS_Map[newCode]).strip()
					#Get codes availables
					ICD9CodesAvailables   = list(localDiagnosisCCSToICD9[codeCCS])
					# Pick random code
					newidx         = random.randint(0, len(ICD9CodesAvailables) - 1)
					newCodeICD9    = str(ICD9CodesAvailables[newidx]).strip()
					newCodeOrdered = CCS_ordered_internalCodesMap[newCodeICD9]
					new_CODEs_List.append(newCodeOrdered)
				
				new_subjectsListOfCODEsList_LIST.append(new_CODEs_List)
			
			new_train_subjectsListOfCODEsList_LIST.append(new_subjectsListOfCODEsList_LIST)
			
	return new_train_subjectsListOfCODEsList_LIST



def makeDataAugmentation(proportion, train_all_subjectsListOfCODEsList_LIST, originalDiagnosisICD9_Codes, CCS_ordered_internalCodesMap, reverse_CCS_ordered_internalCodesMap):	
	icd9TOCCS_Map  = pickle.load(open(sys.path[0]+'/icd9_to_css_dictionary','rb'))
	localDiagnosisCCSToICD9 = {}
	for subject_list_of_CODEs_List in train_all_subjectsListOfCODEsList_LIST:		
		for CODEs_List in subject_list_of_CODEs_List:			
			for CODE in CODEs_List:
				# Get the reverse code of the mapcode
				OriginalCODE = reverse_CCS_ordered_internalCodesMap[CODE]				
				# Get original code
				ICD9_code = originalDiagnosisICD9_Codes[OriginalCODE.strip()]
				
				while (len(ICD9_code) < 6): ICD9_code += ' '  #pad right white spaces because the CCS mapping uses this pattern
				# Get CCS code
				CCS_Code = icd9TOCCS_Map[ICD9_code]
				CCS_Code = ('D' + CCS_Code).strip()
				# Save in dictionary using as key CCS Code
				if CCS_Code in localDiagnosisCCSToICD9:							
					localDiagnosisCCSToICD9[CCS_Code].add(OriginalCODE.strip())
				else:
					localDiagnosisCCSToICD9[CCS_Code] = set()					
					localDiagnosisCCSToICD9[CCS_Code].add(OriginalCODE.strip())

	# Generate data augmentation
	train_all_subjectsListOfCODEsList_LIST = generateDataAugmentation(proportion, train_all_subjectsListOfCODEsList_LIST, CCS_ordered_internalCodesMap, reverse_CCS_ordered_internalCodesMap, localDiagnosisCCSToICD9, originalDiagnosisICD9_Codes)
	
	return train_all_subjectsListOfCODEsList_LIST





	

				
