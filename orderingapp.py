import mysql.connector
from mysql.connector import Error

def connectToDatabase(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful.")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# This is the block of table creation statements
def createUserRoleTable(connection, cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS UserRole (UserRoleID int NOT NULL,RoleDescription varchar(50) UNIQUE,PRIMARY KEY (UserRoleID))")
    connection.commit()
    print("UserRole table created.")

def createUsersTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Users (UserID int NOT NULL, FirstName varchar(100) NOT NULL, LastName varchar(100) NOT NULL, UserRoleID int, UserEmail varchar(100), PreferredPaymentMethod varchar(100), isDeleted BOOLEAN DEFAULT FALSE, PRIMARY KEY (UserID))")
    connection.commit()
    print("Users table created.")

def createDistributionCenterTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  DistributionCenter (SiteID int NOT NULL, DODAddressCode varchar(10), FacilityNo int NOT NULL, FacilityNoLong int, SiteName varchar(255), SitePhone varchar(100), ShippingAddress varchar(255), ShippingAddress2 varchar(255), ShippingAddress3 varchar(255), ShippingAddress4 varchar(255), ShippingCity varchar(255), ShippingState varchar(100), ShippingZip varchar(100), PRIMARY KEY (SiteID))")
    connection.commit()
    print("DistributionCenter table created.")

def createOrdersTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Orders (OrderID int NOT NULL, UserID int, SiteID int, OrderDetails varchar(255), TotalCost decimal(10,2), OrderStatus varchar(255) CHECK (OrderStatus IN ('Pending', 'Completed', 'Canceled')), PRIMARY KEY (OrderID))")
    connection.commit()
    print("Orders table created.")

def createAuthenticationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Authentication (AuthenticationID int NOT NULL, UserID int, HashedPassword varchar(100), LastPasswordChangeDate date, PasswordChangeRequired boolean DEFAULT FALSE, PRIMARY KEY (AuthenticationID))")
    connection.commit()
    print("Authentication table created.")

def createOrderDetailTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  OrderDetail (OrderDetailID int NOT NULL, OrderID int, ProductID int, Quantity int, Customized boolean, CustomizationID int, PRIMARY KEY (OrderDetailID))")
    connection.commit()
    print("OrderDetail table created.")

def createCustomizationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Customization (CustomizationID int NOT NULL, ItemDescription varchar(255), PRIMARY KEY (CustomizationID))")
    connection.commit()
    print("Customization table created.")

def createProductsTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Products (ProductID int NOT NULL, ProductName varchar(255) NOT NULL UNIQUE, ProductColor varchar(100), ItemDescription varchar(255), Price decimal(5,2)  CHECK (Price >= 0), PRIMARY KEY (ProductID))")
    connection.commit()
    print("Products table created.")

def createInventoryTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Inventory (InventoryID int NOT NULL, ProductID int, CurrentStockLevel int NOT NULL CHECK (CurrentStockLevel >= 0), PRIMARY KEY (InventoryID))")
    connection.commit()
    print("Inventory table created.")

def createAuditLogTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  AuditLog (LogID int NOT NULL, UserID int, ActivityType varchar(255), ActivityTimestamp date, AffectedRecordID int, ItemDescription varchar(255), PRIMARY KEY (LogID))")
    connection.commit()
    print("AuditLog table created.")

def createWarehouseNotificationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  WarehouseNotification (NotificationID int NOT NULL, OrderID int, SiteID int, NotificationTimestamp datetime, PRIMARY KEY (NotificationID))")
    connection.commit()
    print("WarehouseNotification table created.")

def createPaymentNotificationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  PaymentNotification (PaymentID int NOT NULL, OrderID int, Timestamp datetime, PRIMARY KEY (PaymentID))")
    connection.commit()
    print("PaymentNotification table created.")

def runAlterStatements(connection, cursor):
    cursor.execute("ALTER TABLE Users ADD FOREIGN KEY (UserRoleID) REFERENCES UserRole (UserRoleID);")
    cursor.execute("ALTER TABLE Authentication ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);")
    cursor.execute("ALTER TABLE Orders ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);")
    cursor.execute("ALTER TABLE Orders ADD FOREIGN KEY (SiteID) REFERENCES DistributionCenter (SiteID);")
    cursor.execute("ALTER TABLE OrderDetail ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);")
    cursor.execute("ALTER TABLE OrderDetail ADD FOREIGN KEY (ProductID) REFERENCES Products (ProductID);")
    cursor.execute("ALTER TABLE OrderDetail ADD FOREIGN KEY (CustomizationID) REFERENCES Customization (CustomizationID);")
    cursor.execute("ALTER TABLE Inventory ADD FOREIGN KEY (ProductID) REFERENCES Products (ProductID);")
    cursor.execute("ALTER TABLE AuditLog ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);")
    cursor.execute("ALTER TABLE WarehouseNotification ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);")
    cursor.execute("ALTER TABLE WarehouseNotification ADD FOREIGN KEY (SiteID) REFERENCES DistributionCenter (SiteID);")
    cursor.execute("ALTER TABLE PaymentNotification ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);")
    connection.commit()
    print("Alter statements successful.")

# Initial Procedure creation
def createProcedureSoftDeleteUser(connection,cursor):
    softDeleteUser = """
    CREATE PROCEDURE IF NOT EXISTS softDeleteUser (IN deletedUserID INT)
    BEGIN
        UPDATE Users
        SET isDeleted = TRUE
        WHERE userID = deletedUserID;
    END
    """
    cursor.execute(softDeleteUser)
    connection.commit()
    print("softDeleteUser procedure created.")

def createProcedurePasswordChangeVerification(connection,cursor):
    passwordChangeVerification = """
    CREATE PROCEDURE IF NOT EXISTS passwordChangeVerification (IN PasswordChangeRequired BOOLEAN)
    BEGIN
        UPDATE Authentication
        SET PasswordChangeRequired = TRUE
        WHERE hashedPassword IS NULL;
    END
    """
    cursor.execute(passwordChangeVerification)
    connection.commit()
    print("passwordChangeVerification procedure created.")

def createViewAdminUsersView(connection,cursor):
    adminUsersView = """
    CREATE OR REPLACE VIEW adminUsersView AS
    SELECT u.userID AS userId, u.firstName AS firstName, u.lastName AS lastName, u.userEmail AS userEmail, u.preferredPaymentMethod AS preferredPaymentMethod, ur.roleDescription AS userRole
        FROM Users u
        JOIN UserRole ur ON u.userRoleID = ur.userRoleID
        WHERE u.isDeleted = FALSE;
    """
    cursor.execute(adminUsersView)
    connection.commit()
    print("adminUsersView view created.")

def createViewAdminInventoryView(connection,cursor):
    adminInventoryView = """
    CREATE OR REPLACE VIEW adminInventoryView AS
        SELECT p.productID AS productId, p.productName AS productName, p.productColor AS productColor, p.itemDescription AS itemDescription, p.price AS price, i.currentStockLevel AS currentStockLevel
        FROM Products p
        JOIN Inventory i ON p.productID = i.productID;
    """
    cursor.execute(adminInventoryView)
    connection.commit()
    print("adminInventoryView view created.")

def createViewUserProfiles(connection,cursor):
    userProfiles = """
    CREATE OR REPLACE VIEW userProfiles AS 
    SELECT users.userID AS userID, users.firstName AS firstName, users.lastName AS lastName, users.userEmail AS userEmail, users.preferredPaymentMethod AS preferredPaymentMethod, userRole.roleDescription AS userRole 
    FROM users 
    JOIN userRole ON users.userRoleID = userRole.userRoleID;
    """
    cursor.execute(userProfiles)
    connection.commit()
    print("userProfiles view created.")

def createViewProductDetailView(connection,cursor):
    productDetailView = """
    CREATE OR REPLACE VIEW productDetailView AS
    SELECT p.productID AS productId, 
           p.productName AS productName, 
           p.productColor AS productColor, 
           p.itemDescription AS itemDescription, 
           p.price AS price, 
           i.currentStockLevel AS currentStockLevel
    FROM Products p
    JOIN Inventory i ON p.productID = i.productID;
    """
    cursor.execute(productDetailView)
    connection.commit()
    print("productDetailView view created.")

def createViewDistributionCenterView(connection,cursor):
    distributionCenterView = """
    CREATE OR REPLACE VIEW distributionCenterView AS
    SELECT s.siteID AS siteId, s.dODAddressCode AS dODAddressCode, s.facilityNo AS facilityNo, s.siteName AS siteName, s.sitePhone AS sitePhone, s.shippingAddress AS shippingAddress, s.shippingCity AS shippingCity, s.shippingState AS shippingState, s.shippingZip AS shippingZip
    FROM DistributionCenter s;
    """
    cursor.execute(distributionCenterView)
    connection.commit()
    print("distributionCenterView view created.")

def createViewOrderView(connection,cursor):
    orderView = """
    CREATE OR REPLACE VIEW orderView AS
    SELECT o.orderID AS orderId, o.userID AS userId, u.firstName AS userFirstName, u.lastName AS userLastName, o.siteID AS siteId, s.siteName AS siteName, o.orderDetails AS orderDetails, o.totalCost AS totalCost, o.orderStatus AS orderStatus
    FROM Orders o
    JOIN Users u ON o.userID = u.userID
    JOIN DistributionCenter s ON o.siteID = s.siteID
    WHERE u.isDeleted = FALSE;
    """
    cursor.execute(orderView)
    connection.commit()
    print("orderView view created.")

def createViewWarehouseNotificationsView(connection,cursor):
    warehouseNotificationsView = """
    CREATE OR REPLACE VIEW warehouseNotificationsView AS 
    SELECT warehouseNotification.notificationID AS notificationID, orders.orderID AS orderID, users.firstName AS firstName, users.lastName AS lastName, warehouseNotification.notificationTimestamp AS notificationTimestamp, distributionCenter.siteName AS siteName FROM warehouseNotification 
    JOIN orders ON warehouseNotification.orderID = orders.orderID 
    JOIN users ON orders.userID = users.userID 
    JOIN distributionCenter ON warehouseNotification.siteID = distributionCenter.siteID;
    """
    cursor.execute(warehouseNotificationsView)
    connection.commit()
    print("warehouseNotificationsView view created.")


def createViewPaymentNotificationsView(connection,cursor):
    paymentNotificationsView = """
    CREATE OR REPLACE VIEW paymentNotificationsView AS 
    SELECT paymentNotification.paymentID AS paymentID, orders.orderID AS orderID, users.firstName AS firstName, users.lastName AS lastName, paymentNotification.timestamp AS timestamp 
    FROM paymentNotification 
    JOIN orders ON paymentNotification.orderID = orders.orderID 
    JOIN users ON orders.userID = users.userID;
    """
    cursor.execute(paymentNotificationsView)
    connection.commit()
    print("paymentNotificationsView view created.")

def createViewUserActivityLogs(connection,cursor):
    userActivityLogs = """
    CREATE OR REPLACE VIEW userActivityLogs AS 
    SELECT auditLog.logID AS logID, users.firstName AS firstName, users.lastName AS lastName, auditLog.activityType AS activityType, auditLog.activityTimestamp AS activityTimestamp, auditLog.itemDescription AS itemDescription 
    FROM auditLog 
    JOIN users ON auditLog.userID = users.userID;
    """
    cursor.execute(userActivityLogs)
    connection.commit()
    print("userActivityLogs view created.")

# Read all from user table
def readAllUsers(cursor):
    sql_query = ("SELECT * FROM users")
    cursor.execute(sql_query)
    print("This is a test to pull all data from users table.")
    print(cursor.fetchall())
    print("Test successful. Congrats, this works.")

if __name__ == "__main__":

    # Replace parameters with DB information
    host_name = "localhost"
    user_name = "root"
    user_password = "SoPAStudentDB!#!"
    db_name = "aafesorder"

    # Initialize database connection
    connection = connectToDatabase(host_name, user_name, user_password, db_name)

    # Initialize database cursor
    cursor = connection.cursor()

    # Create all tables and alter statements
    createUserRoleTable(connection, cursor)
    createUsersTable(connection, cursor)
    createDistributionCenterTable(connection, cursor)
    createOrdersTable(connection, cursor)
    createAuthenticationTable(connection, cursor)
    createOrderDetailTable(connection, cursor)
    createCustomizationTable(connection, cursor)
    createProductsTable(connection, cursor)
    createInventoryTable(connection, cursor)
    createAuditLogTable(connection, cursor)
    createWarehouseNotificationTable(connection, cursor)
    createPaymentNotificationTable(connection, cursor)
    runAlterStatements(connection, cursor)

    # Create procedures
    createProcedureSoftDeleteUser(connection, cursor)
    createProcedurePasswordChangeVerification(connection, cursor)

    # Create views
    createViewAdminUsersView(connection, cursor)
    createViewAdminInventoryView(connection, cursor)
    createViewUserProfiles(connection, cursor)
    createViewProductDetailView(connection, cursor)
    createViewDistributionCenterView(connection, cursor)
    createViewOrderView(connection, cursor)
    createViewPaymentNotificationsView(connection, cursor)
    createViewWarehouseNotificationsView(connection, cursor)
    createViewUserActivityLogs(connection, cursor)


    # Read user table
    readAllUsers(cursor)

    # Closing connection when done
    if connection:
        connection.close()
