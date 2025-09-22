
CREATE OR REPLACE TRIGGER cause_before_update_trigger
BEFORE UPDATE ON cause
FOR EACH ROW
EXECUTE FUNCTION cause_before_update_triggerfn();
