
CREATE OR REPLACE TRIGGER beneficiary_before_insert_trigger
BEFORE INSERT ON beneficiary
FOR EACH ROW
EXECUTE FUNCTION beneficiary_before_insert_triggerfn();
