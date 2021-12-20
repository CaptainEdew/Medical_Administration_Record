DROP DATABASE MAR;
CREATE DATABASE MAR;

CREATE TABLE MAR.dbo.week_of(
week_of_id int IDENTITY(1,1), week_of DATE,
PRIMARY KEY(week_of_id));

CREATE TABLE MAR.dbo.weekdays(
weekday_id int IDENTITY(1,1), day_of_week varchar(10),
PRIMARY KEY(weekday_id));

CREATE TABLE MAR.dbo.admin_time(
admin_time_id int IDENTITY(1,1), admin_time nvarchar(6),
PRIMARY KEY(admin_time_id));

CREATE TABLE MAR.dbo.medications(
medication_id int IDENTITY(1,1), medication varchar(75),
admin_time_id int, PRIMARY KEY(medication_id));

CREATE TABLE MAR.dbo.medication_administration(
week_of_id int, weekday_id int, medication_id int,
med_admin BIT NOT NULL, time_of_admin datetime2, PRIMARY KEY(week_of_id,weekday_id,medication_id),
FOREIGN KEY (week_of_id) REFERENCES MAR.dbo.week_of(week_of_id),
FOREIGN KEY (weekday_id) REFERENCES MAR.dbo.weekdays(weekday_id),
FOREIGN KEY (medication_id) REFERENCES MAR.dbo.medications(medication_id));

CREATE TABLE MAR.dbo.weekdays_stage(weekdays varchar(10));
BULK INSERT MAR.dbo.weekdays_stage
FROM 'C:\Users\andre\Documents\Python Files\MAR\weekdays.txt'
WITH
(
	FIRSTROW = 1,
	ROWTERMINATOR = ',',
	FORMAT = 'CSV'
);

INSERT INTO MAR.dbo.weekdays
SELECT weekdays FROM MAR.dbo.weekdays_stage;
DROP TABLE MAR.dbo.weekdays_stage;

CREATE TABLE MAR.dbo.admin_time_stage(admin_time varchar(6));
BULK INSERT MAR.dbo.admin_time_stage
FROM 'C:\Users\andre\Documents\Python Files\MAR\admin_times.txt'
WITH
(
	FIRSTROW = 1,
	ROWTERMINATOR = ',',
	FORMAT = 'CSV'
);

INSERT INTO MAR.dbo.admin_time
SELECT admin_time FROM MAR.dbo.admin_time_stage;
DROP TABLE MAR.dbo.admin_time_stage;

CREATE TABLE MAR.dbo.medications_stage(medication varchar(75),admin_time_id int);
BULK INSERT MAR.dbo.medications_stage
FROM 'C:\Users\andre\Documents\Python Files\MAR\medications.txt'
WITH
(
	FIRSTROW = 1,
	FORMAT = 'CSV'
);

INSERT INTO MAR.dbo.medications
SELECT medication,admin_time_id FROM MAR.dbo.medications_stage;
DROP TABLE MAR.dbo.medications_stage;