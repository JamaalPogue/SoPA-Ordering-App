SELECT UserID,
    FirstName,
    LastName,
    UserRoleID,
    UserEmail,
    PreferredPaymentMethod,
    isDeleted
FROM users
WHERE UserID = UserIDValue;