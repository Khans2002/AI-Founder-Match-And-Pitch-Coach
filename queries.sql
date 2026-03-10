-- SQL Queries to check the Founders Matchmaking Database
-- -------------------------------------------------------------
-- ⚠️ IMPORTANT NOTE ON VIEWING THIS DATABASE:
-- MySQL Workbench DOES NOT support `.db` (SQLite) files. 
-- To view this database with a GUI, you should use either:
-- 1. "DB Browser for SQLite" (Free app: https://sqlitebrowser.org/)
-- 2. "DBeaver" (Free universal database tool)
-- 3. VS Code Extension: "SQLite" (by alexcvzz)
-- -------------------------------------------------------------

-- 1. View all founder profiles in the network
SELECT * FROM founders;

-- 2. Find only Technical Co-Founders
SELECT * FROM founders 
WHERE role = 'Technical/Software' OR role = 'Hardware Engineering';

-- 3. Find only Business or Operations Co-Founders
SELECT * FROM founders 
WHERE role = 'Business/Marketing' OR role = 'Operations/Finance';

-- 4. Search for specific skills (e.g., Python)
SELECT name, role, skills 
FROM founders 
WHERE skills LIKE '%Python%';

-- 5. Add a new founder manually (Testing)
INSERT INTO founders (name, role, skills, pitch)
VALUES ('Test User', 'Design/Product', 'Figma, Tailwind', 'I want to build an AI interior design app.');

-- 6. Delete a specific founder by ID
-- DELETE FROM founders WHERE id = 5;
