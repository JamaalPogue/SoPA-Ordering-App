CREATE DATABASE AAFESOrder;

CREATE TABLE UserRole (
  UserRoleID int NOT NULL,
  ItemDescription varchar(50),
  PRIMARY KEY (UserRoleID)
);

CREATE TABLE Users (
  UserID int NOT NULL,
  FirstName varchar(100),
  LastName varchar(100),
  UserRoleID int,
  UserEmail varchar(100),
  PreferredPaymentMethod varchar(100),
  PRIMARY KEY (UserID)
);

CREATE TABLE DistributionCenter (
  SiteID int NOT NULL,
  DODAddressCode varchar(10),
  FacilityNo int,
  FacilityNoLong int,
  SiteName varchar(100),
  SitePhone varchar(100),
  ShippingAddress varchar(100),
  ShippingAddress2 varchar(100),
  ShippingAddress3 varchar(100),
  ShippingAddress4 varchar(100),
  ShippingCity varchar(100),
  ShippingState varchar(100),
  ShippingZip varchar(100),
  PRIMARY KEY (SiteID)
);

CREATE TABLE Orders (
  OrderID int NOT NULL,
  UserID int,
  SiteID int,
  OrderDetails varchar(255),
  TotalCost decimal(10,2),
  OrderStatus varchar(255),
  PRIMARY KEY (OrderID)
);

CREATE TABLE Authentication (
  AuthenticationID int NOT NULL,
  UserID int,
  HashedPassword varchar(100),
  LastPasswordChangeDate date,
  PasswordChangeRequired boolean,
  PRIMARY KEY (AuthenticationID)
);

CREATE TABLE OrderDetail (
  OrderDetailID int NOT NULL,
  OrderID int,
  ProductID int,
  Quantity int,
  Customized boolean,
  CustomizationID int,
  PRIMARY KEY (OrderDetailID)
);

CREATE TABLE Customization (
  CustomizationID int NOT NULL,
  ItemDescription varchar(50),
  PRIMARY KEY (CustomizationID)  
);

CREATE TABLE Products (
  ProductID int NOT NULL,
  ProductName varchar(200),
  ProductColor varchar(50),
  ItemDescription varchar(255),
  Price decimal(5,2),
  PRIMARY KEY (ProductID)
);

CREATE TABLE Inventory (
  InventoryID int NOT NULL,
  ProductID int,
  CurrentStockLevel int,
  PRIMARY KEY (InventoryID)
);

CREATE TABLE AuditLog (
  LogID int NOT NULL,
  UserID int,
  ActivityType varchar(255),
  ActivityTimestamp date,
  AffectedRecordID int,
  ItemDescription varchar(255),
  PRIMARY KEY (LogID)
);

CREATE TABLE WarehouseNotification (
  NotificationID int NOT NULL,
  OrderID int,
  SiteID int,
  NotificationTimestamp datetime,
  PRIMARY KEY (NotificationID)
);

CREATE TABLE PaymentNotification (
  PaymentID int NOT NULL,
  OrderID int,
  Timestamp datetime,
  PRIMARY KEY (PaymentID)
);



ALTER TABLE Users ADD FOREIGN KEY (UserRoleID) REFERENCES UserRole (UserRoleID);

ALTER TABLE Authentication ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);

ALTER TABLE Orders ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);

ALTER TABLE Orders ADD FOREIGN KEY (SiteID) REFERENCES DistributionCenter (SiteID);

ALTER TABLE OrderDetail ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);

ALTER TABLE OrderDetail ADD FOREIGN KEY (ProductID) REFERENCES Products (ProductID);

ALTER TABLE OrderDetail ADD FOREIGN KEY (CustomizationID) REFERENCES Customization (CustomizationID);

ALTER TABLE Inventory ADD FOREIGN KEY (ProductID) REFERENCES Products (ProductID);

ALTER TABLE AuditLog ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);

ALTER TABLE WarehouseNotification ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);

ALTER TABLE WarehouseNotification ADD FOREIGN KEY (SiteID) REFERENCES DistributionCenter (SiteID);

ALTER TABLE PaymentNotification ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);

ALTER TABLE users ADD COLUMN isDeleted BOOLEAN DEFAULT FALSE; 


DELIMITER //

CREATE PROCEDURE softDeleteUser (IN deletedUserID INT)
BEGIN
    UPDATE Users
	SET isDeleted = TRUE
	WHERE userID = deletedUserID;
END //

DELIMITER ;

CREATE VIEW adminUsersView AS
SELECT u.userID AS userId, u.firstName AS firstName, u.lastName AS lastName, u.userEmail AS userEmail, u.preferredPaymentMethod AS preferredPaymentMethod, ur.itemDescription AS userRole
FROM Users u
JOIN UserRole ur ON u.userRoleID = ur.userRoleID
WHERE u.isDeleted = FALSE;


CREATE VIEW adminInventoryView AS
SELECT p.productID AS productId, p.productName AS productName, p.productColor AS productColor, p.itemDescription AS itemDescription, p.price AS price, i.currentStockLevel AS currentStockLevel
FROM Products p
JOIN Inventory i ON p.productID = i.productID;


CREATE VIEW userProfiles AS 
SELECT users.userID AS userID, users.firstName AS firstName, users.lastName AS lastName, users.userEmail AS userEmail, users.preferredPaymentMethod AS preferredPaymentMethod, userRole.itemDescription AS userRole 
FROM users 
JOIN userRole ON users.userRoleID = userRole.userRoleID;


CREATE VIEW productDetailView AS
SELECT p.productID AS productId, 
       p.productName AS productName, 
       p.productColor AS productColor, 
       p.itemDescription AS itemDescription, 
       p.price AS price, 
       i.currentStockLevel AS currentStockLevel
FROM Products p
JOIN Inventory i ON p.productID = i.productID;


CREATE VIEW distributionCenterView AS
SELECT s.siteID AS siteId, s.dODAddressCode AS dODAddressCode, s.facilityNo AS facilityNo, s.siteName AS siteName, s.sitePhone AS sitePhone, s.shippingAddress AS shippingAddress, s.shippingCity AS shippingCity, s.shippingState AS shippingState, s.shippingZip AS shippingZip
FROM DistributionCenter s;


CREATE VIEW orderView AS
SELECT o.orderID AS orderId, o.userID AS userId, u.firstName AS userFirstName, u.lastName AS userLastName, o.siteID AS siteId, s.siteName AS siteName, o.orderDetails AS orderDetails, o.totalCost AS totalCost, o.orderStatus AS orderStatus
FROM Orders o
JOIN Users u ON o.userID = u.userID
JOIN DistributionCenter s ON o.siteID = s.siteID
WHERE u.isDeleted = FALSE;


CREATE VIEW paymentNotificationsView AS 
SELECT paymentNotification.paymentID AS paymentID, orders.orderID AS orderID, users.firstName AS firstName, users.lastName AS lastName, paymentNotification.timestamp AS timestamp 
FROM paymentNotification 
JOIN orders ON paymentNotification.orderID = orders.orderID 
JOIN users ON orders.userID = users.userID;


CREATE VIEW warehouseNotificationsView AS 
SELECT warehouseNotification.notificationID AS notificationID, orders.orderID AS orderID, users.firstName AS firstName, users.lastName AS lastName, warehouseNotification.notificationTimestamp AS notificationTimestamp, distributionCenter.siteName AS siteName FROM warehouseNotification 
JOIN orders ON warehouseNotification.orderID = orders.orderID 
JOIN users ON orders.userID = users.userID 
JOIN distributionCenter ON warehouseNotification.siteID = distributionCenter.siteID;


CREATE VIEW userActivityLogs AS 
SELECT auditLog.logID AS logID, users.firstName AS firstName, users.lastName AS lastName, auditLog.activityType AS activityType, auditLog.activityTimestamp AS activityTimestamp, auditLog.itemDescription AS itemDescription 
FROM auditLog 
JOIN users ON auditLog.userID = users.userID;
