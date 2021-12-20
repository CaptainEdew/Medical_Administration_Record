#!/usr/bin/env python
"""*******************************************************
mar_sql.py
Andrew Vaz (andrewvaz.89@gmail.com)
September 29th, 2021, modified November 17th, 2021

A program to track and budget your monthly spending.

*******************************************************"""
import pyodbc
import os

server = os.environ['USERDOMAIN'] 
database = 'MAR'
user = os.environ['USERNAME']
username = f'{server}/{user}'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+server+';TRUSTED_CONNECTION=yes;AUTOCOMMIT=ON')
cursor = cnxn.cursor()

#this function loads data for MAR checkboxes. Initializes and returns empty if beginning of the week
def load_data(date,check_dict):
	cursor.execute('select week_of_id from mar.dbo.week_of where week_of = ?',(date))
	row = cursor.fetchone()
	
	#calls for initialization of weekly med data if blank: new week
	#returns checkbox dictionary
	if row == None:
		cursor.execute('{call MAR.dbo.spWeekInitialize(?)}',(date)).commit()
		return check_dict

	#if data exists for current week, fetches data and returns dictionary
	cursor.execute('select * from mar.dbo.med_admin_view where week_of = ?',(date))
	med_admin_row = cursor.fetchone()
	while (med_admin_row != None):
		if med_admin_row.med_admin == 1:
			check_dict['{}_{}'.format(med_admin_row.medication,med_admin_row.day_of_week)].set(1)
		med_admin_row = cursor.fetchone()
	return check_dict

def medadmin(drug,day,state,current_datetime,this_week):
	
	#finds the correct day of week in database
	cursor.execute('select weekday_id from mar.dbo.weekdays where day_of_week = ?',(day))
	row = cursor.fetchone()
	weekday_id = row.weekday_id

	#finds the medication being administered
	cursor.execute('select medication_id from mar.dbo.medications where medication = ?',(drug))
	row = cursor.fetchone()
	med_id = row.medication_id

	#finds the current week id
	cursor.execute('select week_of_id from mar.dbo.week_of where week_of = ?',(this_week))
	row = cursor.fetchone()
	week_of = row.week_of_id

	#updates database onclick of checkbox
	if state == 1:
		cursor.execute('update mar.dbo.medication_administration set med_admin = 1, time_of_admin = ? where medication_id = ? and weekday_id = ? and week_of_id = ?',(current_datetime,med_id,weekday_id,week_of)).commit()
	else:
		cursor.execute('update mar.dbo.medication_administration set med_admin = 0, time_of_admin = ? where medication_id = ? and weekday_id = ? and week_of_id = ?',(current_datetime,med_id,weekday_id,week_of)).commit()
