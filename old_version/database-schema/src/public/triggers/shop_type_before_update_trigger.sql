
CREATE OR REPLACE TRIGGER shop_type_before_update_trigger
BEFORE UPDATE ON shop_type
FOR EACH ROW
EXECUTE FUNCTION shop_type_before_update_triggerfn();
