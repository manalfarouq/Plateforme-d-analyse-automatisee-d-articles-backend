-- Créer l'utilisateur
CREATE USER articles_user WITH PASSWORD 'ton_mot_de_passe';

-- Créer la base et définir articles_user comme propriétaire
CREATE DATABASE articles_db OWNER articles_user;

\c articles_db;

-- Créer la table users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Donner tous les privilèges sur la base à l'utilisateur
GRANT ALL PRIVILEGES ON DATABASE articles_db TO articles_user;

-- Donner les droits sur le schéma public
GRANT ALL PRIVILEGES ON SCHEMA public TO articles_user;

-- Donner les droits sur la table users
GRANT ALL PRIVILEGES ON TABLE users TO articles_user;

-- Donner accès à la séquence utilisée pour la colonne SERIAL
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO articles_user;




-- Créer la table analysis_logs
CREATE TABLE analysis_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    texte_original TEXT NOT NULL,
    categorie VARCHAR(100) NOT NULL,
    resume TEXT,
    ton VARCHAR(50),
    
    -- Clé étrangère vers users
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) 
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Index pour améliorer les performances
CREATE INDEX idx_analysis_logs_user_id ON analysis_logs(user_id);


-- Donner les droits à l'utilisateur
GRANT ALL PRIVILEGES ON TABLE analysis_logs TO articles_user;
GRANT USAGE, SELECT ON SEQUENCE analysis_logs_id_seq TO articles_user;
