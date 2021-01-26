-- Table: public.dd_character

-- DROP TABLE public.dd_character;

CREATE TABLE public.dd_character
(
    user_id bigint NOT NULL,
    str integer NOT NULL DEFAULT 10,
    dex integer NOT NULL DEFAULT 10,
    con integer NOT NULL DEFAULT 10,
    wis integer NOT NULL DEFAULT 10,
    "int" integer NOT NULL DEFAULT 10,
    cha integer NOT NULL DEFAULT 10,
    CONSTRAINT user_id_unique UNIQUE (user_id)
)

    TABLESPACE pg_default;

ALTER TABLE public.dd_character
    OWNER to postgres;
-- Index: userId_index

-- DROP INDEX public."userId_index";

CREATE INDEX "userId_index"
    ON public.dd_character USING btree
        (user_id ASC NULLS LAST)
    TABLESPACE pg_default;
