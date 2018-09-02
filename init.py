#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 23:08:00 2018

@author: marco
"""

import glob, os
#from account import loadAccount, Account
from account import *
from termcolor import colored
from distutils import util

os.system('clear')

# change working directory
contents = glob.glob('*')
datafolder = 'data'
datapath = './' + datafolder + '/'
if datafolder not in contents:
    os.mkdir(datapath)
os.chdir(datapath)

# get and sort list of available pickles
files = glob.glob('*.pkl')
files = sorted(files,reverse=True)
if not files:
    ans = raw_input('No pickles detected. Create new account? [Y/n] ')
    if util.strtobool(ans) == 1:
        name = raw_input('Account name: ')
        a = Account(name)
    else:
        os.sys.exit()
else:
    print(colored('\nAvailable pickles','blue'))
    for el in files:
        print(el)
    ans = raw_input('\nLoad latest datafile? [Y/n] ')
    if util.strtobool(ans) == 1:
        a = loadAccount(files[0])
        a.dispMovements()
    else:
        os.sys.exit()

os.chdir('..')

# %% Control menu loop
while True:
    if len(a.movements) >= 1:
        ans = raw_input('\nMovement(s): view (v), new (n), edit (e), delete (del)' \
                        '\nMore info: forecast (f)' \
                        '\nAccount: save (s), quit (q)\n')
        if ans == 'n':
            a.inputForAddMovement()
            a.dispMovements()
        elif ans == 'e':
            a.inputForEditMovement()
            a.dispMovements()
        elif ans == 'del':
            a.inputForDelMovements()
            a.dispMovements()
        elif ans == 'v':
            os.system('clear')
            a.dispMovements()
        elif ans == 's':
            a.saveAccount()
            a.dispMovements()
        elif ans == 'f':
            b = inputForForecast(a)
            os.system('clear')
            a.dispMovements()
            b.dispMovements()
        elif ans == 'q':
            os.system('clear')
            break
        else:
            print('Command "' + ans + '" not found')
    else:
        ans = raw_input('\nMovement(s): new (n)' \
                        '\nAccount: quit (q)\n')
        if ans == 'n':
            a.inputForAddMovement()
            a.dispMovements()
        elif ans == 'q':
            os.system('clear')
            break
        else:
            print('Command "' + ans + '" not found')
