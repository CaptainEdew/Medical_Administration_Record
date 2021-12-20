-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================
USE MAR;
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Andrew Vaz
-- Create date: November 2, 2021
-- Description:	Initializes week of med admin
-- =============================================
CREATE PROCEDURE spWeekInitialize 
	@current_week date
AS
BEGIN
	SET NOCOUNT ON;
	INSERT INTO MAR.dbo.week_of(week_of) VALUES (@current_week);

	DECLARE @week_id int
	DECLARE @num_of_meds int
	DECLARE @med_count int
	DECLARE @weekday_id int
	SET @weekday_id = 1
	SET @med_count = 1
	SELECT @num_of_meds = COUNT(*) FROM MAR.dbo.medications
	SELECT @week_id = (SELECT week_of_id from MAR.dbo.week_of where week_of = @current_week)

	WHILE @weekday_id <= 7
	BEGIN
		WHILE @num_of_meds >= @med_count
		BEGIN
			INSERT INTO MAR.dbo.medication_administration(week_of_id,weekday_id,medication_id,med_admin,time_of_admin)
			VALUES (@week_id,@weekday_id,@med_count,0,NULL)
			SET @med_count = @med_count + 1
			IF @med_count > @num_of_meds
			BEGIN
				SET @med_count = 1
				BREAK
			END
		END
		SET @weekday_id = @weekday_id + 1
	END

END
GO
