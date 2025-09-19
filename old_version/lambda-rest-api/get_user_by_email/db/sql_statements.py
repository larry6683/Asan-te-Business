select_app_user = '''
SELECT  au.app_user_id,
        ut.code,
        au.email
FROM    app_user au
INNER JOIN user_type ut ON au.user_type_id = ut.user_type_id
WHERE au.email_hash = digest(lower(%(email)s), 'md5')
'''