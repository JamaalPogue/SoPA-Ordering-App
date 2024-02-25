UPDATE orderdetail
SET
OrderID = OrderID,
ProductID = ProductID,
Quantity = Quantity,
Customized = Customized,
CustomizationID = CustomizationID
WHERE OrderDetailID = OrderDetailIDValue;
