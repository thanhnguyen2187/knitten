SELECT * FROM products;

SELECT * FROM product__yarn;

SELECT y.*, py.yarn_count FROM yarns y
JOIN product__yarn py
ON py.yarn_id = y.id
AND py.product_id = '2cf3f3c2-21db-4926-ad25-16cebca9f3bd';

