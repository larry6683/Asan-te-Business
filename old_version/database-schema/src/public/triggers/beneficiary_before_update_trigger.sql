
CREATE OR REPLACE TRIGGER beneficiary_before_update_trigger
BEFORE UPDATE ON beneficiary
FOR EACH ROW
EXECUTE FUNCTION beneficiary_before_update_triggerfn();
