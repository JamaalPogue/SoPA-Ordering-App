UPDATE users
SET
UserID = UserIDValue,
FirstName = FirstNameValue,
LastName = LastNameValue,
UserRoleID = UserRoleIDValue,
UserEmail = UserEmailValue,
PreferredPaymentMethod = PreferredPaymentMethodValue,
isDeleted = DEFAULT
WHERE UserID = UserIDValue;
