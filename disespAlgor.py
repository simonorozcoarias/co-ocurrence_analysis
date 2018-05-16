#!/usr/bin/env python

######################################################################
#               Implemented by Simon Orozco			                     #
######################################################################
import sys
import math
from apriori import *
from scipy.stats import chisquare


def spatialDistribution(file,distance):
  min_sup = 0.15
  min_conf = 0.3
  negative_min_lift = 1
  positive_min_lift = 1
  positive_total = 0
  negative_total = 0
  group_total = 0
  pairs_total = 0
  db_file = open('DE_results_'+distance+'/databasefinal.txt','w')
  all_rules = open('DE_results_'+distance+'/all_rules.txt','w')
  pos_rules = open('DE_results_'+distance+'/positive_rules.txt','w')
  neg_rules = open ('DE_results_'+distance+'/negative_rules.txt', 'w')
  print "Reading file: "+file
  rules = runModuleAprioriComplete(file,0.15,0.3) # To generate using all transactions
  for rule in rules:
    rule_list = []
    rule_ele, conf = rule
    pre, post = rule_ele
    rule_list = list(pre)+list(post)
    freq_list = []
    for elem in rule_list:
      freq_list.append(frequency(file,str(elem)))
    chi2, p = chisquare(freq_list)
    sup = support(rules,rule_list)
    li = lift(rules,rule)
    if(li > positive_min_lift): #positive analysis
        if(float(chi2) < 0.05  or float(chi2) > 3.84):
            if(p < 0.001):
                if(len(list(pre)) > 0): #if lhs1 is not null
                    if(len(list(pre)) > 1): #if lhs2 is not null
                        group_total += 1
                    else:
                        pairs_total += 1
                positive_total += 1
                pos_rules.write("%s => %s\n"%(str(pre),str(post)))
                db_file.write("%s => %s\n"%(str(pre),str(post)))
    else: 
        if(li < negative_min_lift): #negative analysis
            if(p == 1):
                negative_total += 1
                neg_rules.write("%s => %s\n"%(",".join(list(pre)),",".join(list(post))))
                db_file.write("%s => %s\n"%(",".join(list(pre)),",".join(list(post))))
    all_rules.write("%s=>%s  %f  %f  %f  %f  %f\n"%(",".join(list(pre)),",".join(list(post)),conf,chi2,p,sup,li))
  print "---------------------------------------------------------------------"
  print "INFO: File DE_results/all_rules.txt has following format:"
  print "antecedent=>consequent  confidence  Chi-square  P-value  Support  Lift"
  print "database created in file: DE_results/databasefinal.txt"
  print "Total Positive rules: %d "%(positive_total)
  print "Total Negative rules: %d "%(negative_total)
  print "Total Groups: %d "%(group_total)
  print "Total Pairs %d "%(pairs_total)
  print "---------------------------------------------------------------------"
  db_file.close()
  all_rules.close()
  pos_rules.close()
  neg_rules.close()

def transactionCreation(file,distance):
  f = open(file,'r')
  print "Reading file: "+file
  file_lines = f.readlines()
  transc_file = open('DE_results/transactions.csv','w')
  print('writing transactions in file: DE_results/transactions.csv')
  for line in file_lines:
    line_list = line.split(',')
    transc = line_list[0]
    #latitud
    posx = float(line_list[1].replace('\n','')) 
    #longitud
    posy = float(line_list[2].replace('\n','')) 
    for linej in file_lines:
      line_listj = linej.split(',')
      #latitud
      posxj = float(line_listj[1].replace('\n','')) 
      #longitud
      posyj = float(line_listj[2].replace('\n','')) 
      diffLat = deg2rad(posxj - posx)
      diffLon = deg2rad(posyj - posy)
      a = (math.sin(diffLat/2))**2 + math.cos(deg2rad(posx)) * math.cos(deg2rad(posxj)) * (math.sin(diffLon/2))**2
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
      local_dist = 6371 * c #in kilometers
      local_dist_m = local_dist*1000
      if(local_dist_m <= distance and line_list[0] != line_listj[0]):
        if(line_listj[0] not in transc.split(',')):
          transc += ',' + line_listj[0]
    if(len(transc.split(',')) > 1):
      transc_file.write(transc+'\n')
  f.close()
  transc_file.close()

def deg2rad(deg):
  return deg * (math.pi/180)

def frequency(file,element):
  count = 0
  f = open(file,'r')
  file_lines = f.readlines()
  for line in file_lines:
    line_list = line.split(',')
    if(line_list[0] == element):
      count += 1
  f.close()
  return count 

def support(rules,elem_rule):
    sup=0
    for rule in rules:
        rule_ele, conf = rule
        pre, post = rule_ele
        rule_list = list(pre)+list(post)
        ban=0
        for elem in elem_rule:
            if(elem not in rule_list):
                ban=1
        if(ban==0):
            sup += 1
    return float(sup)/float(len(rules))

def lift(rules,rule):
    rule_ele, conf = rule
    a, b = rule_ele
    b_list = list(b)
    pb=0
    for one_rule in rules:
        rule_ele_gnra, conf = one_rule
        pre, pos = rule_ele_gnra
        list_gnra = list(pre)+list(pos)
        ban=0
        for elem in b_list:
            if(elem not in list_gnra):
                ban=1
        if(ban == 0):
            pb += 1
    pb = float(pb)/float(len(rules))
    return float(conf)/float(pb)
    

if __name__ == "__main__":
  if(len(sys.argv) < 3):
    print "Usage: python "+sys.argv[0]+" data.txt distance"
  else:
    print "Cheking if DE_results folder exists..."
    if not os.path.exists('DE_results'):
      print "Folder doesn't exist, creating..."
      os.makedirs('DE_results')
    else:
      print "Folder exists..."
    print "Creating transaction file..."
    transactionCreation(sys.argv[1],float(sys.argv[2]))
    print "done."
    distance=sys.argv[2]
    print "Executing Spatial Distribution analysis...."
    spatialDistribution('DE_results_'+distance+'/transactions.csv',distance)
    print "done."
