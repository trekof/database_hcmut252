-- Initialize demo users for the Library Management System
-- Run this after creating tables and inserting sample data

-- Create Users table if it doesn't exist
CREATE TABLE IF NOT EXISTS Users (
    IDUser INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('Admin', 'NhanVienDungQuay', 'KhachHang') NOT NULL,
    ReferenceID VARCHAR(20),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Clear existing demo users (optional)
DELETE FROM Users WHERE Username IN ('admin', 'cashier', 'customer');

-- Insert demo users with hashed passwords (SHA256 using MySQL SHA2 function)
INSERT INTO Users (Username, Password, Role, ReferenceID, IsActive) VALUES
('admin', SHA2('admin123', 256), 'Admin', 'NV001', TRUE),
('cashier', SHA2('cashier123', 256), 'NhanVienDungQuay', 'NV002', TRUE),
('customer', SHA2('customer123', 256), 'KhachHang', 'KH001', TRUE);

-- Note: Passwords are hashed with MySQL SHA2 function
-- Demo credentials:
-- Admin: admin / admin123
-- Cashier: cashier / cashier123
-- Customer: customer / customer123