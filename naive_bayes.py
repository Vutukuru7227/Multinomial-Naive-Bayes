#!/usr/bin/env python3.5

import os
import sys
import re
import collections
import math

from stop_words import get_stop_words

stopping_words = get_stop_words("english")

training_path = sys.argv[1]
testing_path = sys.argv[2]

labels = list()
files_per_label = list()
class_vocabulary = list()

total_number_of_files = 0

labels_prior_list = list()

vocabulary  	= list()
vocabulary2  	= list()
dir_list    	= list()
lTmp        	= list()
data_files_list = list ()
lWholeVocab     = list ()

vocab_dict 		 	= collections.OrderedDict ()            # Vocabulary of all documents in a category
files_per_class_dict 	 	= collections.OrderedDict ()  # Holds the number of documents per training category
prob_each_class_dict 		= collections.OrderedDict ()       # probability of each class
prob_each_word_in_class_dict    = collections.OrderedDict ()    # holds probability of each word in a category
coll_counter			= collections.OrderedDict ()

temp_files_list = os.listdir (training_path)

for items in temp_files_list:

    if not items.startswith("."):

        dir_list.append(items)

dir_list.sort()

for category in dir_list:
	
	data_files_list		= []
	vocabulary		= []
	vocabulary2		= []
	
	os.chdir (os.path.join(training_path, category))
	
	for x in os.listdir ():
		
		if not x.startswith("."):
			
			data_files_list.append(x)
	
	data_files_list.sort()
	
	total_number_of_files = total_number_of_files + len (data_files_list)
	
	files_per_class_dict [category] = len (data_files_list)
	
	for filename in data_files_list:
		
		with open(filename, 'r', encoding='utf-8', errors='backslashreplace') as data:
			    
			flag = False
            
			for line in data.readlines ():
				
				if flag == False:
					
					if line.startswith('Lines'):
                        		
						flag = True
				
				else:
					
					# consider alpha numeric chars only
					#vocabulary.extend (re.sub('[^a-zA-Z0-9\n\']', ' ', line).lower.strip().split())
					vocabulary.extend(line.lower().strip().split())
	
	for key in vocabulary:
		
		if key not in stopping_words:
			
			vocabulary2.append (key)
	
	lWholeVocab    = lWholeVocab + vocabulary2
	
	if category not in vocab_dict:
		
		vocab_dict [category] = vocabulary2
		
		coll_counter [category]	= collections.Counter (vocabulary2)
	
	else:
		
		print ("Found key in vocab_dict!!!FATAL!!!")

#print (coll_counter)

setWholeVocab_unique  = set (lWholeVocab)

#print (vocab_dict)
#print (len (lWholeVocab))
#print (len (setWholeVocab_unique))
#print (files_per_class_dict)
#print (total_number_of_files)

for category in files_per_class_dict:
	
	prob_each_class_dict [category]  = files_per_class_dict [category] / total_number_of_files

#print (prob_each_class_dict)

# Testing coding goes below

fTmp		= 0.0
dir_list	= []
temp_files_list = os.listdir (testing_path)
test_dict	= collections.OrderedDict ()

for items in temp_files_list:
	
	if not items.startswith("."):
		
		dir_list.append(items)

dir_list.sort()

test_dir_dict			= collections.OrderedDict ()
total_number_of_test_files	= 0

for item in dir_list:
	
	data_files_list = []
	vocabulary 	= []
	vocabulary2	= []
	os.chdir (os.path.join(testing_path, item))
	
	for x in os.listdir():
		
		if not x.startswith("."):
			
			data_files_list.append(x)
		
		data_files_list.sort()
	
	total_number_of_test_files = total_number_of_test_files + len (data_files_list)
	
	for filename in data_files_list:
        	
		#print ("filename = " + filename)
		
		test_dir_dict [filename] = item
		
		vocabulary	= []
		vocabulary2	= []
		
		lTmp2		= []
		lTmp3		= []
		
		with open(filename, 'r', encoding='utf-8', errors='backslashreplace') as data:
			
			fTmp 	= 0.0
			flag	= False
			
			for line in data.readlines():
				
				if flag == False:
					
					if line.startswith('Lines'):
						                        			
						flag = True
				
				else:
					
					# consider alpha numeric chars only
					#vocabulary.extend(re.sub('[^a-zA-Z0-9\n\']', ' ', line).lower().strip().split())
					vocabulary.extend(line.lower().strip().split())
			
			for key in vocabulary:
				
				if key not in stopping_words:
					
					vocabulary2.append (key)
			
			for category in vocab_dict:
				
				fTmp	= 0.0
				
				sTmp    = "%s/%s" %(category, filename)
				
				for word in vocabulary2:
					
					try:
						
						iTmp3	= coll_counter [category][word]
						
						fTmp4	= (iTmp3 + 1) / (len (vocab_dict [category]) + len (setWholeVocab_unique))
						
						fTmp = fTmp + math.log (fTmp4)
					
					except Exception as e:
						
						raise (e)
				
				lTmp2.append (math.log (prob_each_class_dict[category]) + fTmp)
				lTmp3.append (sTmp)
		
		index	= lTmp2.index (max (lTmp2))
		
		test_dict [lTmp3 [index].split ('/')[1]] = lTmp3 [index].split ('/')[0]

#print (test_dict)

iCounter	= 0

for key in test_dict:
	
	if test_dict [key] == test_dir_dict [key]:
		
		iCounter	= iCounter + 1

print ('Accuracy = %.6f' %((iCounter / total_number_of_test_files) * 100))
