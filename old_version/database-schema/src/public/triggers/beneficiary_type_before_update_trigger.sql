
CREATE OR REPLACE TRIGGER beneficiary_type_before_update_trigger
BEFORE UPDATE ON beneficiary_type
FOR EACH ROW
EXECUTE FUNCTION beneficiary_type_before_update_triggerfn();
