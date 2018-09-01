#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 19:16:28 2018

@author: marco
"""

from __future__ import print_function
from termcolor import colored
import datetime as dt
import numpy as np
import pickle
import os, sys, glob


#%% Define class Movement

class Movement:
    
    def __init__(self, date, amount, description, category):
        self.date = date
        self.amount = amount
        self.description = description
        self.category = category
        self.balance = 0
        self.id = '0'
        

#%% Define class Acccount

class Account:
    
    def __init__(self, name):
        self.name = name
        self.movements = []
        self.last_id = 0
        
#%% edit functions
            
    def addMovement(self, date, amount, description, category):
        m    = Movement(date, amount, description, category)
        m.id = str(self.last_id + 1)
        self.last_id += 1
        self.movements.append(m)
        self.update()
        
    def editMovement(self, idx, date, amount, description, category):
        self.movements[idx].date = date
        self.movements[idx].amount = amount
        self.movements[idx].description = description
        self.movements[idx].category = category
        self.update()
        
    def delMovements(self, ID):
        
        # ---> ID is a string.
        # ---> If 2 values separated by '-': delete all movements which are
        #      (chronologically!) bounded by the two values
        # ---> If N comma-separated values: delete single movements
        
        ID.replace(' ','') # remove white spaces within string
        
        batch_ids = ID.split('-')
        single_ids = ID.split(',')
        
        if len(batch_ids) != 1 and len(single_ids) != 1:    # if multiple batch mode
            print('Multiple batch mode not yet supported!')
            
        elif len(single_ids) == 1 and len(batch_ids) != 1:  # if batch mode
            idcs = []
            for idx, el in enumerate(self.movements):
                if str(int(el.id)) in batch_ids:
                    idcs.append(idx)
            if len(idcs) != 2:
                print('Wrong input IDs.')
            else:
                del self.movements[idcs[0]:idcs[1]+1]
            
        elif len(batch_ids) == 1:                           # if singular mode
            idcs = []
            for idx, el in enumerate(self.movements):
                if str(int(el.id)) in single_ids:
                    idcs.append(idx)
            self.movements = [el for idx, el in enumerate(self.movements) if idx not in idcs]
                    
        self.update()

#%% update functions

    # recursively update balance list array based on new movement list
    def updateBalance(self):
        self.movements[0].balance = self.movements[0].amount
        for idx, el in enumerate(self.movements[1::]):
            el.balance = self.movements[idx].balance + el.amount
            
    # recursively update id codes
    def updateID(self):
        for el in self.movements:
            el.id = el.id.zfill(len(str(self.last_id)))
        
    # function that sorts db based on entry date
    def sortMovements(self):
        self.movements.sort(key=lambda movs: map(int, str(movs.date).split('-')))
        
    # combine update functions
    def update(self):
        self.sortMovements()
        self.updateBalance()
        self.updateID()
        
#%% display function
        
    # diplay list of movements
    def dispMovements(self):
        
        if sys.stdin.isatty():  # only if function called from terminal
            printHashLine()     ######### print hash line #############
        
        # define headers
        headers = ['ID', 'date', 'amount', 'balance', 'description', 'category']
        
        # calculate width of column elements
        col_width = [[len(el) for el in headers]]
        for el in self.movements:
            col_width.append([len(str(el.__dict__[field.lower()])) for field in headers])

        # calculate maximum column width
        max_width = np.amax(col_width, axis=0)

        # print header
        header = ''
        for idx, el in enumerate(headers):
            if type(self.movements[0].__dict__[el.lower()])==float:
                header = '  '.join( [header, el.rjust(max_width[idx])] )
            else:
                header = '  '.join( [header, el.ljust(max_width[idx])] )
        print(colored(header,'blue'))
        
        # print data
        for entry in self.movements:
            string = ''
            for idx, el in enumerate(headers):
                if type(entry.__dict__[el.lower()])==float:
                    if entry.__dict__[el] >= 0:
                        string = '  '.join( [string, colored(str(entry.__dict__[el]).rjust(max_width[idx]),'green')] )
                    elif entry.__dict__[el] < 0:
                        string = '  '.join( [string, colored(str(entry.__dict__[el]).rjust(max_width[idx]),'red')] )
                else:
                    string = '  '.join( [string, str(entry.__dict__[el.lower()]).ljust(max_width[idx])] )
            print(string)
            
#%% input functions

    def inputForAddMovement(self):
        
        if sys.stdin.isatty(): # only if function called from terminal
            os.system('clear')
        
        if len(self.movements) >= 1:
            self.dispMovements()
            
        # input movement date
        yy, mm, dd = inputDate()
            
        if not yy:
            yy = dt.date.today().year
        if not mm:
            mm = dt.date.today().month
        if not dd:
            dd = dt.date.today().day
        date = dt.date(int(yy), int(mm), int(dd))
            
        print('Date: ' + str(date))
        
        # input movement amount
        amount = inputAmount()
        
        # input movement description
        description = raw_input('Description: ')
        
        # input movement category
        category = raw_input('Tag: extra, house, daily, saldo? ')
        
        # add movement to account
        self.addMovement(date, amount, description, category)
        
        if sys.stdin.isatty():  # only if function called from terminal
            printHashLine()     ######### print hash line #############
            
        print('New movement successfully added.')
        
        
    def inputForEditMovement(self):
        
        if sys.stdin.isatty(): # only if function called from terminal
            os.system('clear')
        
        self.dispMovements()
        
        ans = raw_input('\nEnter movement to edit: ')
        
        # find movement to edit
        for idx, el in enumerate(self.movements):
            if int(el.id) == int(ans):
                i = idx
        
        # input movement data - no entry confirms previous value
        yy, mm, dd = inputDate()
        
        if not yy and not mm and not dd:
            date = self.movements[i].date
        else:    
            if not yy:
                yy = dt.date.today().year
            if not mm:
                mm = dt.date.today().month
            if not dd:
                dd = dt.date.today().day
            date = dt.date(int(yy), int(mm), int(dd))
            
        print('Date: ' + str(date))
    
        # edit movement amount - no entry confirms previous value
        amount = inputAmount()
        if not amount:
            amount = self.movements[i].amount
        
        # edit movement description - no entry confirms previous value
        description = raw_input('Description: ')
        if not description:
            description = self.movements[i].description
        
        # edit movement category - no entry confirms previous value
        category = raw_input('Tag: extra, house, daily, saldo? ')
        if not category:
            category = self.movements[i].category
        
        self.editMovement(i, date, amount, description, category)
        
        if sys.stdin.isatty():  # only if function called from terminal
            printHashLine()     ######### print hash line #############
            
        print('Movement successfully edited.')
        
        
    def inputForDelMovements(self):
        
        if sys.stdin.isatty(): # only if function called from terminal
            os.system('clear')
        
        self.dispMovements()
        
        ans = raw_input('\nEnter movements to delete [id1-id2 for batch / id1,...,idN for single entries]: ')
        
        self.delMovements(ans)
    
#    def input
        
        
#%% write/read functions

    def saveAccount(self):
        
        if sys.stdin.isatty(): # only if function called from terminal
            os.system('clear')
            
        now = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = self.name + '-' + now + '.pkl'
        with open('./data/' + filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        
        if sys.stdin.isatty():  # only if function called from terminal
            printHashLine()     ######### print hash line #############
            
        print('File successfully saved as "' + filename + '".')
        

def loadAccount(filename):
    
    if sys.stdin.isatty(): # only if function called from terminal
            os.system('clear')
            
    with open(filename, 'rb') as input:
        a = pickle.load(input)
        
    if sys.stdin.isatty():  # only if function called from terminal
        printHashLine()     ######### print hash line #############
            
    print('File "' + filename + '" successfully loaded.')
    
    return a

def inputDate():
    
    print('\n')
        
    # input year and error handling
    
    flag = False
    
    while flag is False:
        
        yy = raw_input('Year: ')
        
        if yy:
            try:
                int(yy)
                flag = True
            except:
                print('\033[A                \033[A')
                print(colored('Year must be an integer!','red'))
        else:
            flag = True
        
    flag = False
        
    # input month and error handling
    
    while flag is False:
        
        mm = raw_input('Month: ')
        
        if mm:
            if int(mm) > 12 or int(mm) <= 0:
                print('\033[A                \033[A')
                print(colored('There are only twelve months, you know.','red'))
            else:
                try:
                    int(mm)
                    flag = True
                except:
                    print('\033[A                \033[A')
                    print(colored('Month must be integer!','red'))
        else:
            flag = True
        
    # input day and error handling
        
    flag = False
    
    while flag is False:
        
        dd = raw_input('Day: ')
        
        if dd:
            if int(dd) > 31 or int(dd) <= 0:
                print('\033[A                \033[A')
                print(colored('No month has ever lived that long.','red'))
            else:
                try:
                    int(dd)
                    flag = True
                except:
                    print('\033[A                \033[A')
                    print(colored('Day must be integer!','red'))
        else:
            flag = True
        
    return yy, mm, dd

# input an amount and check convertibility to float

def inputAmount():
    
    flag = False
    
    while flag is False:
    
        amount = raw_input('Amount: ')
        
        if amount:
            try:
                float(amount)
                flag = True
            except:
                print('\033[A                 \033[A')
                print(colored('Amount must be a number.','red'))
        else:
            flag = True
            
    amount = float(amount)
    
    return amount


def printHashLine():
    rows, columns = os.popen('stty size', 'r').read().split()
    hashes = '#' * int(columns)
    print('\n' + hashes + '\n')

        
#%% Main

def main():
    
    a = Account('ABNAMRO')
    
    date1 = dt.date(2018, 8, 10)
    a.addMovement(date1, 1000, 'Ambarabacciccicocamdmd', 'balubalu')
    
    date3 = dt.date(2018,8,5)
    a.addMovement(date3, -100, 'asd', 'asd')
    
    a.inputForDelMovements()    
    a.dispMovements()
    a.saveAccount()
    
def main2():
    datapath = './data/'
    os.chdir(datapath)
    files = glob.glob('*.pkl')
    files = sorted(files,reverse=True)
    a = loadAccount(files[0])
    a.dispMovements()
    a.inputForAddMovement()
    
if __name__ == '__main__':
    a = main2()
