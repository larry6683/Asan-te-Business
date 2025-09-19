
CREATE OR REPLACE TRIGGER beneficiary_shop_before_update_trigger
BEFORE UPDATE ON beneficiary_shop
FOR EACH ROW
EXECUTE FUNCTION beneficiary_shop_before_update_triggerfn();
