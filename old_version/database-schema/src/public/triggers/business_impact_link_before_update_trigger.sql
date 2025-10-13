
CREATE OR REPLACE TRIGGER business_impact_link_before_update_trigger
BEFORE UPDATE ON business_impact_link
FOR EACH ROW
EXECUTE FUNCTION business_impact_link_before_update_triggerfn();
