DROP TABLE IF EXISTS phonebook;
DROP PROCEDURE IF EXISTS insert_or_update_user;
DROP PROCEDURE IF EXISTS insert_many_users;
DROP FUNCTION IF EXISTS get_users_by_pattern;
DROP FUNCTION IF EXISTS get_paginated_users;
DROP PROCEDURE IF EXISTS delete_user;

CREATE TABLE phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50),
    phone VARCHAR(20)
);

CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_surname TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(name, surname, phone) VALUES(p_name, p_surname, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_users(user_list TEXT[][])
LANGUAGE plpgsql AS $$
DECLARE
    user_data TEXT[];
    invalid_users TEXT[] := '{}';
BEGIN
    FOREACH user_data SLICE 1 IN ARRAY user_list
    LOOP
        IF user_data[3] ~ '^\d{11}$' THEN
            CALL insert_or_update_user(user_data[1], user_data[2], user_data[3]);
        ELSE
            invalid_users := array_append(invalid_users, user_data[1] || ' ' || user_data[2]);
        END IF;
    END LOOP;

    RAISE NOTICE 'Invalid entries: %', invalid_users;
END;
$$;

CREATE OR REPLACE FUNCTION get_users_by_pattern(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    WHERE name ILIKE '%' || pattern || '%'
       OR surname ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$;

CREATE OR REPLACE FUNCTION get_paginated_users(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT p_limit OFFSET p_offset;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_user(p_keyword TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_keyword OR surname = p_keyword OR phone = p_keyword;
END;
$$;

DROP TABLE IF EXISTS phonebook;DROP PROCEDURE IF EXISTS insert_or_update_user;DROP PROCEDURE IF EXISTS insert_many_users;DROP FUNCTION IF EXISTS get_users_by_pattern;DROP FUNCTION IF EXISTS get_paginated_users;DROP PROCEDURE IF EXISTS delete_user;CREATE TABLE phonebook (    id SERIAL PRIMARY KEY,    name VARCHAR(50),    surname VARCHAR(50),    phone VARCHAR(20));CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_surname TEXT, p_phone TEXT)LANGUAGE plpgsql AS $$BEGIN    IF EXISTS (        SELECT 1 FROM phonebook WHERE name = p_name AND surname = p_surname    ) THEN        UPDATE phonebook SET phone = p_phone        WHERE name = p_name AND surname = p_surname;    ELSE        INSERT INTO phonebook(name, surname, phone) VALUES(p_name, p_surname, p_phone);    END IF;END;$$;CREATE OR REPLACE PROCEDURE insert_many_users(user_list TEXT[][])LANGUAGE plpgsql AS $$DECLARE    user_data TEXT[];    invalid_users TEXT[] := '{}';BEGIN    FOREACH user_data SLICE 1 IN ARRAY user_list    LOOP        IF user_data[3] ~ '^\d{11}$' THEN            CALL insert_or_update_user(user_data[1], user_data[2], user_data[3]);        ELSE            invalid_users := array_append(invalid_users, user_data[1] || ' ' || user_data[2]);        END IF;    END LOOP;    RAISE NOTICE 'Invalid entries: %', invalid_users;END;$$;CREATE OR REPLACE FUNCTION get_users_by_pattern(pattern TEXT)RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT)LANGUAGE plpgsql AS $$BEGIN    RETURN QUERY    SELECT * FROM phonebook    WHERE name ILIKE '%' || pattern || '%'       OR surname ILIKE '%' || pattern || '%'       OR phone ILIKE '%' || pattern || '%';END;$$;CREATE OR REPLACE FUNCTION get_paginated_users(p_limit INT, p_offset INT)RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT)LANGUAGE plpgsql AS $$BEGIN    RETURN QUERY    SELECT * FROM phonebook    ORDER BY id    LIMIT p_limit OFFSET p_offset;END;$$;CREATE OR REPLACE PROCEDURE delete_user(p_keyword TEXT)LANGUAGE plpgsql AS $$BEGIN    DELETE FROM phonebook    WHERE name = p_keyword OR surname = p_keyword OR phone = p_keyword;END;$$;


