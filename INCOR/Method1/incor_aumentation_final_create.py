import numpy as np
import math
import cPickle as pickle
import random
import argparse
import entropy_analysis
from copy import copy

def makeDataAugmentation(train_all_subjectsListOfCODEsList_LIST):
	# Start the method
	
	onlyTwoAdmissionsPatients = []
	for patient_admissions in train_all_subjectsListOfCODEsList_LIST:
		nAdms = len(patient_admissions)
		ithAdm = 0
		# Creating subsequences
		while (ithAdm < (nAdms - 1)):
			twoAdmis = []
			twoAdmis.append(patient_admissions[ithAdm])
			twoAdmis.append(patient_admissions[ithAdm + 1])
			ithAdm += 1
			onlyTwoAdmissionsPatients.append(twoAdmis)

	train_all_subjectsListOfCODEsList_LIST = train_all_subjectsListOfCODEsList_LIST + onlyTwoAdmissionsPatients
	
	return train_all_subjectsListOfCODEsList_LIST