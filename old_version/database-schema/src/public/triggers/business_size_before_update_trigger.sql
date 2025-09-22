
CREATE OR REPLACE TRIGGER business_size_before_update_trigger
BEFORE UPDATE ON business_size
FOR EACH ROW
EXECUTE FUNCTION business_size_before_update_triggerfn();
