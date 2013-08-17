#!/usr/bin/env python
#coding: utf-8

import sys, shelve

def storePerson(db):
    """
    Query user for data and store it in the shelf object
    """

    pid = raw_input('Enter unique ID number: ')
    person = {}
    person['name'] = raw_input('Enter name: ')
    person['age'] = raw_input('Enter age: ')
    person['phone'] = raw_input('Enter phone number: ')

    db[pid] = person

def lookupPerson(db):
    '''
    Query user for ID and desired field. and fetch the corresponding data from
    the shelf object
    '''
    pid = raw_input('Enter ID number: ')
    field = raw_input('What would you like to know? (name, age, or phone)')
    field = field.strip().lower()
    print field.capitalize() + ':', \