
CREATE OR REPLACE TRIGGER cause_category_before_update_trigger
BEFORE UPDATE ON cause_category
FOR EACH ROW
EXECUTE FUNCTION cause_category_before_update_triggerfn();
