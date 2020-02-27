import sys
import cPickle as pickle
import os

if __name__ == '__main__':
	# ACHF
	ccsTOicd9_Map = {}

	icd9TOccs_Map = {}
	ccsTOdescription_Map = {}
	#'ICD-9-CM CODE','CCS CATEGORY','CCS CATEGORY DESCRIPTION','ICD-9-CM CODE DESCRIPTION','OPTIONAL CCS CATEGORY','OPTIONAL CCS CATEGORY DESCRIPTION'
	dxref_ccs_file = open(sys.path[0]+'/CCS/$dxref 2015.csv', 'r')
	dxref_ccs_file.readline() #note
	dxref_ccs_file.readline() #header
	dxref_ccs_file.readline() #null
	for line in dxref_ccs_file:
		tokens = line.strip().split(',')
		# since diagnosis and procedure ICD9 codes have intersections, a prefix is necessary for disambiguation
		icd9TOccs_Map['D'+str(tokens[0][1:-1])] = str(tokens[1][1:-1])			#[1:-1] retira aspas
		ccsTOdescription_Map[str(tokens[1][1:-1])] = str(tokens[2][1:-1])		#[1:-1] retira aspas


		idccsToicd9 = 'D'+str(tokens[1][1:-1])
		if idccsToicd9 in ccsTOicd9_Map:
			ccsTOicd9_Map[idccsToicd9].add(str(tokens[0][1:-1]))
		else:
			ccsTOicd9_Map[idccsToicd9] = set()
			ccsTOicd9_Map[idccsToicd9].add(str(tokens[0][1:-1]))

		

	dxref_ccs_file.close()

	dxprref_ccs_file = open(sys.path[0]+'/CCS/$prref 2015.csv', 'r')
	dxprref_ccs_file.readline() #note
	dxprref_ccs_file.readline() #header
	dxprref_ccs_file.readline() #null
	for line in dxprref_ccs_file:
		tokens = line.strip().split(',')
		#since diagnosis and procedure ICD9 codes have intersections, a prefix is necessary for disambiguation
		icd9TOccs_Map['P'+str(tokens[0][1:-1])] = str(tokens[1][1:-1])			#[1:-1] retira aspas
		ccsTOdescription_Map[str(tokens[1][1:-1])] = str(tokens[2][1:-1])		#[1:-1] retira aspas

		idccsToicd9 = 'P'+str(tokens[1][1:-1])
		if idccsToicd9 in ccsTOicd9_Map:
			ccsTOicd9_Map[idccsToicd9].add(str(tokens[0][1:-1]))
		else:
			ccsTOicd9_Map[idccsToicd9] = set()
			ccsTOicd9_Map[idccsToicd9].add(str(tokens[0][1:-1]))


	dxprref_ccs_file.close()

	print('ccsTOicd9_Map: ')
	print(ccsTOicd9_Map)

	pickle.dump(icd9TOccs_Map, open(sys.path[0]+'/icd9_to_css_dictionary', 'wb'), -1)
	pickle.dump(ccsTOicd9_Map, open(sys.path[0]+'/css_to_icd9_dictionary', 'wb'), -1)
	pickle.dump(ccsTOdescription_Map, open(sys.path[0]+'/ccs_to_description_dictionary', 'wb'), -1)
	print 'Total icd9 to ccs entries: ' + str(len(icd9TOccs_Map))
	print 'Total ccs codes/descriptions: ' + str(len(ccsTOdescription_Map))