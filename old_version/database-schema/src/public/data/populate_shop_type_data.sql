/*
    script populating definitions for shop types
*/
DO
LANGUAGE plpgsql
$$
DECLARE
    shopify_code          CONSTANT    INT    := 1;
BEGIN
    
    /*
        save shop types
    */
    CALL    save_shop_type(shopify_code, 'shopify');

END 
$$;

/*
QUERIES

select * from shop_type
*/