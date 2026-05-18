USE sims;

INSERT INTO users (name, email, password, role) VALUES
('admin', 'admin', '$2b$12$V.X8vR8rIwx6Q3H8NzfVgeER2S9caM57Yf3PtlYhKtyu1ukI7IXwy', 'admin'),
('employee', 'employee', '$2b$12$V.X8vR8rIwx6Q3H8NzfVgeER2S9caM57Yf3PtlYhKtyu1ukI7IXwy', 'employee');

INSERT INTO suppliers (supplier_name, phone, email, address) VALUES
('FreshFoods Ltd', '1234567890', 'contact@freshfoods.com', '12 Market Street'),
('TechSource', '0987654321', 'sales@techsource.com', '44 Innovation Ave');

INSERT INTO products (name, category, quantity, price, supplier_id) VALUES
('Rice Bag 5kg', 'Groceries', 50, 18.99, 1),
('Wireless Mouse', 'Electronics', 20, 14.50, 2),
('USB Keyboard', 'Electronics', 4, 19.99, 2);

INSERT INTO sales (product_id, quantity, total_price) VALUES
(1, 2, 37.98),
(2, 1, 14.50);
