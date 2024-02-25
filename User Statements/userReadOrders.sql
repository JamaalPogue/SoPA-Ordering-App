SELECT OrderID,
    UserID,
    SiteID,
    OrderDetails,
    TotalCost,
    OrderStatus
FROM orders
WHERE OrderID = OrderIDValue;