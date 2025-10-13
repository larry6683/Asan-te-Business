
CREATE OR REPLACE TRIGGER business_before_update_trigger
BEFORE UPDATE ON business
FOR EACH ROW
EXECUTE FUNCTION business_before_update_triggerfn();
