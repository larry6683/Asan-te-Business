
CREATE TABLE IF NOT EXISTS public.app_user_registration_type
(
    app_user_registration_type_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    app_user_id                   UUID NOT NULL REFERENCES public.app_user(app_user_id),
    registration_type_id          UUID NOT NULL REFERENCES public.registration_type(registration_type_id),
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
