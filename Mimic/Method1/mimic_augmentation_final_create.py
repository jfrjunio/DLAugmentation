import math
import sys
import cPickle as pickle
import random
from copy import copy
import numpy as np

def makeDataAugmentation(train_all_subjectsListOfCODEsList_LIST):
	# Starts data augmentation
	onlyTwoAdmissionsPatients = []
	for patient_admissions in train_all_subjectsListOfCODEsList_LIST:
		nAdms = len(patient_admissions)
		ithAdm = 0
		# Creating subsequences
		while(ithAdm < (nAdms-1)):
			twoAdmis = []
			twoAdmis.append(patient_admissions[ithAdm])
			twoAdmis.append(patient_admissions[ithAdm+1])
			ithAdm += 1
			onlyTwoAdmissionsPatients.append(twoAdmis)

	train_all_subjectsListOfCODEsList_LIST = train_all_subjectsListOfCODEsList_LIST + onlyTwoAdmissionsPatients	
	
	return train_all_subjectsListOfCODEsList_LIST