
CREATE OR REPLACE TRIGGER business_user_before_update_trigger
BEFORE UPDATE ON business_user
FOR EACH ROW
EXECUTE FUNCTION business_user_before_update_triggerfn();
