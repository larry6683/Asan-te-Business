
CREATE OR REPLACE TRIGGER user_type_before_update_trigger
BEFORE UPDATE ON user_type
FOR EACH ROW
EXECUTE FUNCTION user_type_before_update_triggerfn();
