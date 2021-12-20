USE MAR;

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER audit_trace_initialization
ON medication_administration
AFTER INSERT AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @week_of_id INT
	DECLARE @weekday_id INT
	DECLARE @med_id INT
	DECLARE @med_admin BIT
	DECLARE @time_of_change DATETIME2
	SET @time_of_change = GETDATE()
	DECLARE @initialization BIT
	SELECT @initialization = 1
	SELECT @med_admin = (SELECT med_admin FROM INSERTED)
	SELECT @med_id = (SELECT medication_id FROM INSERTED)
	SELECT @weekday_id = (SELECT weekday_id FROM INSERTED)
	SELECT @week_of_id = (SELECT week_of_id FROM INSERTED)

	INSERT INTO med_admin_audit VALUES (@week_of_id,@weekday_id,@med_id,@med_admin,@time_of_change,@initialization)
END