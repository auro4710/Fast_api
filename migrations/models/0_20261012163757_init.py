from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlV9P2zAUxb9KlScmsQlCGWhvpRqCaWslKNOkabKc5Dax6tjBdjYQ5Lvj6yQ4TUu1Sm"
    "h/EE9tzj227/3JJ7kLcpkA1++uNKjgw+AuEDQH+2dJ3x0EtCi8ioKhEXfGsnVE2igaG6vN"
    "KddgpQR0rFhhmBRWFSXnKMrYGplIvVQKdl0CMTIFk7k+vv+wMhMJ3IBuH4sFmTPgyVKbLM"
    "GznU7MbeG0c2FOnRFPi0gseZkLby5uTSbFo5sJg2oKAhQ1gNsbVWL72F0zZTtR3am31C12"
    "1iQwpyU3nXEj4rWAkMl0Ri4/zggJtgAUS4FwbavaTZ9iC2/D/eHR8Pjg/fDYWlybj8pRVR"
    "/twdQLHZ7JLKhcnRpaOxxjD9X9rmAdZ1St59r6e2Rty32yLcd/F21ObwgHkZrMPu7v7W0A"
    "+XV0MT4bXexY1xs8UtrrX2di0pTCulZVeH/niw5sFCIaL35RlZCVigzlU97VUh7mfYUKmj"
    "p0OCRO0KR5BIrF2bqcN5WNSafe85r1l5L1n6A0trRF3DtLnifxreAJ+1v1xzMfHh7+Ruat"
    "68nMuxpS95QxVFsQbuwvkO6zvVG7dO2JBupoLxP+dDmdrCfcWdKjnLDYDO4HnOmVd8V/QH"
    "sDXISBO+daX/Mu050vo2993OPP0xMHR2qTKreL2+Dkb3/Mqgesx2TA"
)
