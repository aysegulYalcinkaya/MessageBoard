CREATE TABLE IF NOT EXISTS public.tb_user
(
    id SERIAL PRIMARY KEY,
    email character varying(120) NOT NULL,
    password character varying(50) NOT NULL,
    CONSTRAINT tb_user_email_key UNIQUE (email)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public.tb_mail
(
    id SERIAL PRIMARY KEY,
    user_id integer NOT NULL,
    mail_content character varying(2000) NOT NULL,
    CONSTRAINT tb_user_fk FOREIGN KEY (user_id)
        REFERENCES public.tb_user (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
TABLESPACE pg_default;


