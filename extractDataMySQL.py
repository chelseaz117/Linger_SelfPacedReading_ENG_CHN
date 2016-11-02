#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import _mysql
import sys

debug = 0
def DatabaseConnection():
    return mdb.connect('localhost', 'root', 'mysql', '')

def DatabaseCreateExperimentDataTable(): #the template
    cmd = "DROP DATABASE IF EXISTS Experiments; "
    cmd += "CREATE DATABASE Experiments; "
    cmd += "USE Experiments; "
    cmd += "CREATE TABLE IF NOT EXISTS ExperimentDefinition("
    cmd += "ID CHAR(255) NOT NULL PRIMARY KEY, "
    cmd += "Name CHAR(255), "
    cmd += "ExpGroup CHAR(255), "
    cmd += "OriginalNumber INT, "
    cmd += "MainFill CHAR(255), "
    cmd += "RCtype CHAR(255), "
    cmd += "Plausibility CHAR(255), "
    cmd += "Demonstrative CHAR(255), "
    cmd += "Passive CHAR(255), "
    cmd += "region1 CHAR(255), "
    cmd += "region2 CHAR(255), "
    cmd += "de1 CHAR(255), "
    cmd += "dem CHAR(255), "
    cmd += "NP1 CHAR(255), "
    cmd += "de2 CHAR(255), "
    cmd += "NP2 CHAR(255), "
    cmd += "end CHAR(255), "
    cmd += "Questions CHAR(255)"
    cmd += ")"

    if debug == 1:
        print cmd
    try:
        con = DatabaseConnection()
        cur = con.cursor()
        cur.execute(cmd)
        if debug == 1:
            print cur.fetchall()
        print "OKAY: DatabaseCreateExperimentDataTable"
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        print "FAIL: DatabaseCreateExperimentDataTable"
        sys.exit(1)
    finally:
        if debug == 1:
            print "Closing cur, con"
        cur.close()

def DatabaseImportExperimentDataTable():
    con = DatabaseConnection()
    cur = con.cursor()
    cmd = "USE Experiments; "
    cur.execute(cmd)

    dataName = raw_input("Enter Experiment Data(L1A, L1B, L2A or L2B): ")
    fname = raw_input("Enter Experiment Data File: ")
    file = open(fname, "r")
    number = 0
    for line in file:
        cmd = "INSERT INTO ExperimentDefinition(ID, ExpGroup,OriginalNumber,MainFill,RCtype,Plausibility,Demonstrative,Passive,region1,region2,de1,dem,NP1,de2,NP2,end,Questions) VALUES"
        number = number + 1
        id = dataName + "-" + str(number)
        cmd += "(\"" + id + "\", \"" + line.replace(",", "\",\"") + "\")"
        cmd += ";"
        if debug == 1:
            print cmd
        cur.execute(cmd)
    con.commit()
    con.close()
    print "OKAY: DatabaseImportExperimentDataTable"

def DatabaseCreateResultDataTable(): #the result
    cmd = "USE Experiments; "
    cmd += "CREATE TABLE IF NOT EXISTS Results("
    cmd += "ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
    cmd += "SentenceID CHAR(255), "
    cmd += "Name CHAR(255), "
    cmd += "Type CHAR(255), "
    cmd += "SentenceNumber CHAR(255), "
    cmd += "WordNumber CHAR(255), "
    cmd += "Word CHAR(255), "
    cmd += "Time BIGINT"
    cmd += ")"

    if debug == 1:
        print cmd
    try:
        con = DatabaseConnection()
        cur = con.cursor()
        cur.execute(cmd)
        if debug == 1:
            print cur.fetchall()
        print "OKAY: DatabaseCreateResultDataTable"
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        print "FAIL: DatabaseCreateResultDataTable"
        sys.exit(1)
    finally:
        if debug == 1:
            print "Closing cur, con"
        cur.close()

def DatabaseImportResultDataTable():
    con = DatabaseConnection()
    cur = con.cursor()
    cmd = "USE Experiments; "
    cur.execute(cmd)

    dataName = raw_input("Enter Experiment Data(L1A, L1B, L2A or L2B): ")
    fname = raw_input("Enter result file name: ")
    file = open(fname, "r")
    for line in file:
        cmd = "INSERT INTO Results(SentenceID, Name, Type, SentenceNumber, WordNumber, Word, Time) VALUES"
        words = line.split()
        name = fname + words[0]
        type = words[1]
        sentenceNumber = words[2]
        wordNumber = words[4]
        word = words[5]
        time = words[7]
        sentenceId = dataName + "-" + sentenceNumber
        cmd += "(\"" + sentenceId + "\", \"" + name + "\", \"" + type + "\", \"" + sentenceNumber + "\", \"" + wordNumber + "\", \"" + word + "\", \"" + time  + "\")"
        cmd += ";"
        if debug == 1:
            print cmd
        cur.execute(cmd)
    con.commit()
    con.close()
    print "OKAY: DatabaseImportResultDataTable"

def DatabaseInitialization():
    DatabaseCreateExperimentDataTable()
    DatabaseImportExperimentDataTable()
    DatabaseCreateResultDataTable()
    DatabaseImportResultDataTable()

def printOptions():
    print ""
    print "What do you want to do? Enter number below: "
    print "0: Quit"
    print "1: Create Tables"
    print "2: Import New Experiment Data"
    print "3: Import New Result"

def main():
    while True:
        printOptions()
        selection = raw_input()
        if selection == "1":
            DatabaseCreateExperimentDataTable()
            DatabaseCreateResultDataTable()
        elif selection == "2":
            DatabaseImportExperimentDataTable()
        elif selection == "3":
            DatabaseImportResultDataTable()
        else:
            break

main()

