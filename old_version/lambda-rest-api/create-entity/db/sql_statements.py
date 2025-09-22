select_app_user = '''
SELECT  app_user_id,
        ut.code
FROM    public.app_user au
INNER JOIN public.user_type ut on au.user_type_id = ut.user_type_id
WHERE   app_user_id = %(app_user_id)s
'''

select_business_user_info = '''
SELECT  bu.app_user_id,
        b.business_id,
        business_name
FROM    business_user bu
INNER JOIN  Business b On b.business_id = bu.business_id
WHERE   bu.app_user_id = %(app_user_id)s
'''

select_beneficiary_user_info = '''
SELECT  bu.app_user_id,
        b.beneficiary_id,
        b.beneficiary_name
FROM    beneficiary_user bu
INNER JOIN  Beneficiary b On b.beneficiary_id = bu.beneficiary_id
WHERE   bu.app_user_id = %(app_user_id)s
'''

select_business_name = '''
SELECT  business_id,
        business_name
FROM    business
WHERE   business_name_hash = digest(lower(%(business_name)s), 'md5')
'''
select_beneficiary_name = '''
SELECT  beneficiary_id,
        beneficiary_name
FROM    beneficiary
WHERE   beneficiary_name_hash = digest(lower(%(beneficiary_name)s), 'md5')
'''

select_business_email = '''
SELECT  email
FROM    business
WHERE   email_hash = digest(lower(%(email)s), 'md5')
'''

insert_org_sql = {}
insert_org_sql['business'] = '''
INSERT INTO public.business (
        business_name, 
        email, 
        phone_number, 
        location_city, 
        location_state, 
        website_url,
        business_size_id
    ) VALUES (
        %(business_name)s, 
        %(email)s, 
        %(phone_number)s, 
        %(location_city)s, 
        %(location_state)s, 
        %(website_url)s,
        (
            SELECT business_size_id
            FROM business_size
            WHERE code = %(business_size_code)s
        )
    ) RETURNING business_id;
'''
insert_org_sql['beneficiary'] = '''
INSERT INTO public.beneficiary (
        beneficiary_name, 
        email, 
        phone_number, 
        location_city, 
        location_state, 
        website_url,
        beneficiary_size_id
    ) 
    VALUES (
        %(beneficiary_name)s, 
        %(email)s, 
        %(phone_number)s, 
        %(location_city)s, 
        %(location_state)s, 
        %(website_url)s,
        (
            SELECT beneficiary_size_id
            FROM beneficiary_size
            WHERE code = %(beneficiary_size_code)s
        )
    ) RETURNING beneficiary_id;
'''

insert_org_user_sql_template = '''
INSERT INTO public.{org_type}_user(
    {org_type}_id,
    app_user_id,
    {org_type}_user_permission_role_id
)
VALUES (
    %(entity_id)s,
    %(app_user_id)s,
    (
        SELECT {org_type}_user_permission_role_id
        FROM {org_type}_user_permission_role
        WHERE code = %(user_permission_role_code)s
    )
)
'''

insert_org_user_sql = {
    org_type: insert_org_user_sql_template.format(org_type=org_type) 
    for org_type in ['business', 'beneficiary']
}

insert_cause_preference_sql_template = '''
INSERT INTO public.{org_type}_cause_preference (
    {org_type}_id, 
    cause_id,
    cause_preference_rank_id
)
VALUES (
    %(entity_id)s,
    (
        SELECT cause_id 
        FROM cause 
        WHERE code = %(cause_code)s
    ),
    (
        SELECT cause_preference_rank_id
        FROM cause_preference_rank
        WHERE code = %(cause_preference_rank_code)s
    )
)
'''

insert_cause_preference_sql = {
    org_type: insert_cause_preference_sql_template.format(org_type=org_type)
    for org_type in ['business', 'beneficiary']
}

insert_org_shop_sql_template = '''
INSERT INTO public.{org_type}_shop(
    {org_type}_id,
    shop_type_id,
    shop_url
)
VALUES (
    %(entity_id)s,
    (
        SELECT shop_type_id
        FROM shop_type
        WHERE code = %(shop_type_code)s
    ),
    %(shop_url)s
)
'''

insert_org_shop_sql = {
    org_type: insert_org_shop_sql_template.format(org_type=org_type) 
    for org_type in ['business', 'beneficiary']
}

insert_social_media_sql_template = '''
INSERT INTO public.{org_type}_social_media(
        {org_type}_id,
        social_media_type_id,
        social_media_url
    )
	VALUES (
        %(entity_id)s,
        (
            SELECT social_media_type_id 
            FROM social_media_type 
            WHERE code = %(social_media_type_code)s
        ),
        %(social_media_url)s
    );
'''
insert_social_media_sql = {
    org_type: insert_social_media_sql_template.format(org_type=org_type) 
    for org_type in ['business', 'beneficiary']
}