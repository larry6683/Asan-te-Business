
CREATE OR REPLACE TRIGGER app_user_before_insert_trigger
BEFORE INSERT ON app_user
FOR EACH ROW
EXECUTE FUNCTION app_user_before_insert_triggerfn();
