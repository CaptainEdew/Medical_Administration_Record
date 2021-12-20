SELECT        dbo.medications.medication, dbo.week_of.week_of, dbo.weekdays.day_of_week, dbo.medication_administration.med_admin
FROM            dbo.medication_administration INNER JOIN
                         dbo.medications ON dbo.medication_administration.medication_id = dbo.medications.medication_id INNER JOIN
                         dbo.week_of ON dbo.medication_administration.week_of_id = dbo.week_of.week_of_id INNER JOIN
                         dbo.weekdays ON dbo.medication_administration.weekday_id = dbo.weekdays.weekday_id