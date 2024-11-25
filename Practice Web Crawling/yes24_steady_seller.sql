show databases;
USE yes24_steady;
SHOW TABLES;  -- 테이블 목록 확인
SELECT * FROM books;  -- 데이터 확인

USE yes24_steady;

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_rank INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    pub_date VARCHAR(50) NOT NULL,
    price VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

USE yes24_steady;
SELECT COUNT(*) FROM books;
SELECT * FROM books;