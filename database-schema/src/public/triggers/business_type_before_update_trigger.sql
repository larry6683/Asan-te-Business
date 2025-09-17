
CREATE OR REPLACE TRIGGER business_type_before_update_trigger
BEFORE UPDATE ON business_type
FOR EACH ROW
EXECUTE FUNCTION business_type_before_update_triggerfn();
