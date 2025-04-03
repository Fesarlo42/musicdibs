CREATE DATABASE IF NOT EXISTS musicdibs 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
USE musicdibs;

-- All users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User verification token for email confirmation
CREATE TABLE IF NOT EXISTS verification_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE
);

-- Music genres
CREATE TABLE IF NOT EXISTS genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- General entity to hold information about the music projects
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP
);

-- Project genres
CREATE TABLE IF NOT EXISTS project_genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) 
        ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) 
        ON DELETE CASCADE
);

-- Uploaded files
CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    path VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) 
        ON DELETE CASCADE
);

-- Conversation with AI
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    project_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    tempo VARCHAR(50) NOT NULL,
    key_signature VARCHAR(50) NOT NULL,
    mood VARCHAR(50) NOT NULL,
    status ENUM('in_progress', 'completed', 'archived') DEFAULT 'in_progress',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) 
        ON DELETE CASCADE
);

-- Conversation messages
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    is_from_ai BOOLEAN NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) 
        ON DELETE CASCADE
);

-- Blockchain registration
CREATE TABLE IF NOT EXISTS registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    ibs_id VARCHAR(255) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) 
        ON DELETE CASCADE
);

-- Credit history
CREATE TABLE IF NOT EXISTS credit_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('credit', 'debit') NOT NULL,
    amount INT NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE
);