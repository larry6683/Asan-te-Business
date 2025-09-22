
CREATE OR REPLACE TRIGGER beneficiary_size_before_update_trigger
BEFORE UPDATE ON beneficiary_size
FOR EACH ROW
EXECUTE FUNCTION beneficiary_size_before_update_triggerfn();
