-- 仅重置 handbook_mysql_lab 中本课程拥有的表。不要用于真实业务库。
CREATE DATABASE IF NOT EXISTS handbook_mysql_lab
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE handbook_mysql_lab;
DROP TABLE IF EXISTS handbook_mysql_lab.lab_messages;
DROP TABLE IF EXISTS handbook_mysql_lab.lab_conversations;
DROP TABLE IF EXISTS handbook_mysql_lab.quota_rules;
DROP TABLE IF EXISTS handbook_mysql_lab.import_items;
DROP TABLE IF EXISTS handbook_mysql_lab.import_progress;
DROP TABLE IF EXISTS handbook_mysql_lab.credit_events;
DROP TABLE IF EXISTS handbook_mysql_lab.accounts;
DROP TABLE IF EXISTS handbook_mysql_lab.lock_numbers;
DROP TABLE IF EXISTS handbook_mysql_lab.tasks;
DROP TABLE IF EXISTS handbook_mysql_lab.members;
CREATE TABLE handbook_mysql_lab.members (
 id BIGINT PRIMARY KEY,
 tenant_id BIGINT NOT NULL,
 name VARCHAR(40) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE handbook_mysql_lab.tasks (
 id BIGINT PRIMARY KEY,
 tenant_id BIGINT NOT NULL,
 owner_id BIGINT NULL,
 title VARCHAR(100) NOT NULL,
 status VARCHAR(16) NOT NULL DEFAULT 'pending',
 priority INT NOT NULL DEFAULT 1,
 created_at DATETIME NOT NULL
) ENGINE=InnoDB;
INSERT INTO handbook_mysql_lab.members VALUES
 (1,10,'小林'),(2,10,'小周'),(3,20,'小陈');
INSERT INTO handbook_mysql_lab.tasks VALUES
 (1,10,1,'整理笔记','pending',2,'2026-09-01 09:00:00'),
 (2,10,1,'修复登录','done',1,'2026-09-01 10:00:00'),
 (3,10,2,'练习 SQL','pending',3,'2026-09-02 09:00:00'),
 (4,10,NULL,'写周报','pending',1,'2026-09-02 10:00:00'),
 (5,20,3,'导入文档','pending',2,'2026-09-03 09:00:00'),
 (6,10,2,'整理测试','done',2,'2026-09-04 09:00:00');
CREATE TABLE handbook_mysql_lab.accounts (
 id INT PRIMARY KEY,
 credits INT NOT NULL,
 version INT NOT NULL DEFAULT 0,
 CONSTRAINT ck_accounts_credits CHECK (credits >= 0)
) ENGINE=InnoDB;
INSERT INTO handbook_mysql_lab.accounts VALUES (1,100,0),(2,100,0);
CREATE TABLE handbook_mysql_lab.credit_events (
 id INT PRIMARY KEY,
 account_id INT NOT NULL,
 amount INT NOT NULL
) ENGINE=InnoDB;
CREATE TABLE handbook_mysql_lab.lock_numbers (id INT PRIMARY KEY) ENGINE=InnoDB;
INSERT INTO handbook_mysql_lab.lock_numbers VALUES (10),(20),(30);
