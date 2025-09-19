
CREATE OR REPLACE TRIGGER beneficiary_user_before_update_trigger
BEFORE UPDATE ON beneficiary_user
FOR EACH ROW
EXECUTE FUNCTION beneficiary_user_before_update_triggerfn();
