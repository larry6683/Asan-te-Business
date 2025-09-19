insert_user_sql = '''
INSERT INTO app_user (email, mailing_list_signup, user_type_id)
VALUES (
    %(email)s, 
    %(mailing_list_signup)s, 
    (
        SELECT user_type_id
        FROM user_type
        WHERE code = %(user_type_code)s
    )
)
returning app_user_id, 
email, 
(   
    SELECT  code 
    FROM user_type 
    WHERE user_type_id = user_type_id 
    LIMIT 1
)
'''

select_existing_user_sql = '''
SELECT email
FROM app_user
WHERE email_hash = digest(lower(%(email)s), 'md5')
'''