-- Populate dev database

USE musicdibs;

-- Add Users
INSERT INTO users ( password, email, first_name, last_name, role, is_active) 
VALUES 
('admin123', 'admin@example.com', 'Admin', 'User', 'admin', TRUE),
('password123', 'jj@example.com', 'Jack', 'Johnson', 'user', TRUE);

-- Add Credits for the user
INSERT INTO credit_transactions (user_id, type, amount, transaction_date)
VALUES
(2, 'debit', 5, '2024-03-01 10:00:00'),  
(2, 'credit', 10, '2024-03-02 15:30:00'),  
(2, 'debit', 8, '2024-03-05 08:45:00'),  
(2, 'credit', 15, '2024-03-07 20:10:00'),  
(2, 'debit', 12, '2024-03-10 14:25:00'),  
(2, 'credit', 5, '2024-03-12 18:00:00');  

-- Add Genres
-- Seed music genres
INSERT INTO genres (name) VALUES
('Pop'),
('Rock'),
('Hip Hop'),
('Rap'),
('R&B'),
('Jazz'),
('Blues'),
('Country'),
('Electronic'),
('Dance'),
('House'),
('Techno'),
('Classical'),
('Reggae'),
('Soul'),
('Funk'),
('Metal'),
('Punk'),
('Folk'),
('Indie'),
('Latin'),
('K-Pop'),
('Gospel'),
('Disco'),
('Trap');