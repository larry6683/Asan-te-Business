
CREATE OR REPLACE TRIGGER social_media_type_before_update_trigger
BEFORE UPDATE ON social_media_type
FOR EACH ROW
EXECUTE FUNCTION social_media_type_before_update_triggerfn();
