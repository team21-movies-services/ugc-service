
CREATE TABLE IF NOT EXISTS "users_favorites" (
    id Serial Primary Key,
    user_id UUID,
    film_id UUID
);
