#!/usr/bin/python
#encoding: utf-8

import MySQLdb as mdb
import _mysql
import sys

def DatabaseConnection():
    return mdb.connect('localhost', 'root', 'mysql', 'experiments', charset='utf8')

def main():    
    reload(sys)
    sys.setdefaultencoding('utf-8')
    con = DatabaseConnection()
    cur = con.cursor()
    cmd = """select time, word, wordNumber from ExperimentDefinition e inner join results r where e.ID = r.sentenceId AND Demonstrative = 'DEM-' AND RCtype = 'ACTIVE' AND Plausibility = 'EQUI' AND MainFill = 'MAIN' AND OriginalNumber < 9 AND wordNumber = 0;"""
    cur.execute(cmd)
    fname = "test.txt"
    file = open(fname, "w")
    count = 0
    while (1):
    	row = cur.fetchone()
    	if row == None: 
    		break
    	print>>file, str(row).decode('utf8')
    	count = count + 1
    print count
    cur.close()
    con.close()
main()