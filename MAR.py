#!/usr/bin/env python
"""*******************************************************
MAR.py
Andrew Vaz (andrewvaz.89@gmail.com)
September 1st, 2021, modified September 29th, 2021

Simple UI to log personal medication administration.

*******************************************************"""
import tkinter as tk
import datetime
from tkinter import font
import mar_sql

class MAR(tk.Frame):

	def __init__(self,master):
		tk.Frame.__init__(self,master)

		self.grid()

		#fonts
		self.medication_list_label_font = font.Font(family='Arial',size=10,underline=True)

		#window frames
		self.date_frame = tk.Frame(master)
		self.main_frame = tk.Frame(master)
		self.day_label_frame = tk.Frame(self.main_frame)
		self.med_label_frame = tk.Frame(self.main_frame)
		self.check_frame = tk.Frame(self.main_frame)
		
		self.day_list_abrv = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
		self.day_list_full = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
		self.med_list = ['Drug 1','Drug 2','Drug 3']
		self.week_of_var = ''
		self.set_date()

		#dictionaries for labels,check buttons and check variables
		self.day_dict = {}
		self.check_dict = {}
		self.check_var_dict = {}
		self.med_dict = {}
		
		#master grid config
		self.master.rowconfigure(0,weight=1)
		self.master.rowconfigure(1,weight=8)
		self.master.columnconfigure(0,weight=1)
		self.master.grid_propagate(False)

		#set frames in master grid
		self.date_frame.grid(row=0,column=0,sticky='news')
		self.main_frame.grid(row=1,column=0,sticky='news')
		self.date_frame.grid_propagate(False)
		self.main_frame.grid_propagate(False)

		#master frames grid config
		self.date_frame.rowconfigure(0)
		self.date_frame.columnconfigure(0,weight=7)
		self.date_frame.columnconfigure(1,weight=3)
		self.main_frame.columnconfigure(0,weight=3)
		self.main_frame.columnconfigure(1,weight=7)

		for x in range(len(self.med_list)+1):
			self.main_frame.rowconfigure(x,weight=1)

		#set frames in main_frame grid
		self.med_label_frame.grid(row=0,column=0,rowspan=len(self.med_list)+1,sticky='news')
		self.day_label_frame.grid(row=0,column=1,sticky='news')
		self.check_frame.grid(row=1,column=1,rowspan=len(self.med_list),sticky='news')
		self.day_label_frame.grid_propagate(False)
		self.med_label_frame.grid_propagate(False)
		self.check_frame.grid_propagate(False)

		#configuring grid for frames
		self.day_label_frame.rowconfigure(0,weight=1)
		self.med_label_frame.columnconfigure(0,weight=1)
		
		for x in range(len(self.day_list_abrv)):
			self.day_label_frame.columnconfigure(x,weight=1)
			self.check_frame.columnconfigure(x,weight=1)
		
		for x in range(len(self.med_list)+1):
			if x == 0:
				self.med_label_frame.rowconfigure(x,weight=1)
			else:
				self.med_label_frame.rowconfigure(x,weight=1)
				self.check_frame.rowconfigure(x-1,weight=1)

		#creates date_frame labels
		self.week_label = tk.Label()
		self.week_of_label = tk.Label(self.date_frame,text='Week of {}'.format(self.week_of_var))
		self.current_datetime = tk.Label(self.date_frame,text=datetime.date.today().strftime('%m/%d/%Y'))

		self.medication_list_label = tk.Label(self.med_label_frame,text='Medications',font=self.medication_list_label_font)
		self.medication_list_label.grid(row=0,column=0,sticky='news')

		#creates day labels 
		for day in self.day_list_abrv:
			self.day_dict['{}_label'.format(day)] = tk.Label(self.day_label_frame, text=day)

		#creates med labels
		for med in self.med_list:
			self.med_dict['{}_label'.format(med)] = tk.Label(self.med_label_frame, text=med)
		
		#sets days in grid
		for x,item in zip(range(len(self.day_list_abrv)),self.day_dict):
			self.day_dict[item].grid(row=0,column=x,sticky='news')

		#sets drugs in grid
		for x,drug in zip(range(len(self.med_list)),self.med_dict):
			self.med_dict[drug].grid(row=x+1,column=0,sticky='news')
		
		#creates checkbuttons for med admin/sets in grid
		for drug,x in zip(self.med_list,range(len(self.med_list))):
			for day,y in zip(self.day_list_full,range(len(self.day_list_abrv))):
				self.check_var_dict['{}_{}'.format(drug,day)] = tk.IntVar()
				self.check_dict['{}_{}'.format(drug,day)] = tk.Checkbutton(self.check_frame,variable = self.check_var_dict['{}_{}'.format(drug,day)],
															command=lambda drug=drug,day=day:self.medadmin(drug,day))
				self.check_dict['{}_{}'.format(drug,day)].grid(row=x,column=y,sticky='news')

		#set remaining widgets in grid
		self.week_of_label.grid(row=0,column=0,sticky='news')
		self.current_datetime.grid(row=0,column=1,sticky='e')

		self.load_data()
		self.disable_checkboxes(datetime.date.today())

	def set_date(self):
		cur_date = datetime.date.today()
		weekday_num = datetime.date.weekday(cur_date)
		if weekday_num == 6:
			self.week_of_var = cur_date.strftime('%m/%d/%Y')
		else:
			day_of_year = cur_date.toordinal()
			current_sunday_day_num = day_of_year - (weekday_num+1)
			self.week_of_var = datetime.date.fromordinal(current_sunday_day_num).strftime('%m/%d/%Y')

	def load_data(self):
		self.check_var_dict = mar_sql.load_data(self.week_of_var,self.check_var_dict)

	def medadmin(self,drug,day):
		if self.check_var_dict['{}_{}'.format(drug,day)].get() == 1:
			self.check_var_dict['{}_{}'.format(drug,day)].set(1)
		else:
			self.check_var_dict['{}_{}'.format(drug,day)].set(0)

		mar_sql.medadmin(drug,day,self.check_var_dict['{}_{}'.format(drug,day)].get(),datetime.datetime.now(),self.week_of_var)

	def disable_checkboxes(self,today_date):
		current_weekday_index = datetime.date.weekday(today_date) #gets current weekday number via datetime
		#if block corrects weekday index to personal standard
		if current_weekday_index == 6:
			current_weekday_index = 0
		else:
			current_weekday_index += 1

		#for loop disables checkboxes if it has been set or if it is too late to set
		for box in self.check_var_dict:
			start_index = box.find('_') #find the "_" in key, which precedes the weekday text
			weekday_text = box[start_index+1:] #gets text of weekday
			weekday_index = self.day_list_full.index(weekday_text) #index of day in list, this is so we can correctly calculate the day of week number specified in datetime
			if self.check_var_dict[box].get() == 1 or today_date.toordinal() > today_date.toordinal()+(weekday_index-current_weekday_index):
				self.check_dict[box].config(state=tk.DISABLED)

root = tk.Tk()
root.title('Medical Administration Records')
root.geometry('400x150')
root.resizable(False,False)
MAR(master=root)
root.mainloop()