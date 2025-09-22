
CREATE OR REPLACE TRIGGER business_shop_before_update_trigger
BEFORE UPDATE ON business_shop
FOR EACH ROW
EXECUTE FUNCTION business_shop_before_update_triggerfn();
