
CREATE OR REPLACE TRIGGER business_before_insert_trigger
BEFORE INSERT ON business
FOR EACH ROW
EXECUTE FUNCTION business_before_insert_triggerfn();
