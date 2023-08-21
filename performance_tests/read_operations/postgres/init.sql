
CREATE TABLE IF NOT EXISTS "users_favorites" (
    id Serial Primary Key,
    user_id UUID,
    film_id UUID
);

CREATE UNIQUE INDEX user_films_uniq ON users_favorites USING btree (user_id, film_id);
