def test_should_validate_password_when_plain_password_passed(self, reseller):
    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    validation_instance = reseller.verify_password(
        "Pwd@123", reseller.password
    )
    validation_ctx = ctx.verify("Pwd@123", reseller.password)
    assert validation_instance == validation_ctx
