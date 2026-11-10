from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `age` INT NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP COLUMN `age`;"""


MODELS_STATE = (
    "eJztlV9P2zAUxb9KlScmbRNkZSDeSrVpm7ZWgm6ahCbLSW4Tq44d7JsNBP3us50Ep+kfqM"
    "QEnXhqcu6xff2rfXIT5DIBrt9+16CCk95NIGgO5mFBf90LaFF41QpII+6MZeOINCoao9Gm"
    "lGswUgI6VqxAJoVRRcm5FWVsjEykXioFuyyBoEwBM9fHxS8jM5HAFejmtZiRKQOeLLTJEr"
    "u20wleF077LPCjM9rVIhJLXubCm4trzKS4czOBVk1BgKIIdnpUpW3fdlfvstlR1am3VC22"
    "xiQwpSXH1nYj4rWAkNF4Qs4/TAgJtgAUS2Hhmla1231qW3gTHvSP+sfv3vePjcW1eaccza"
    "ulPZhqoMMzmgRzV6dIK4dj7KG63yWsw4yq1Vwbf4esablLtuH4fNHm9IpwEClm5vVgf38D"
    "yB+Ds+Gnwdmecb2yS0pz/Ks7MapLYVWztD1dmq6Au/bM1u77D+1D0DaCZ+uv6o6cW5sE01"
    "nr2FohovHsD1UJWarIUK7zLpfyMO8qVJg/IKl3ZJurc3EAisXZqsSsKxszk3rPS2ru0unb"
    "lJq/QWnb0hbB2RryONn51Bd8IT3Dw8MHpKdxrU1PV+ukp7lUWxCu7f8h3X/ybTIrIlRXe5"
    "Hwl/PxaDXh1pAO5YTF2LvtcaZ38WO1Aa6FYWfOtb7kbaZ73wY/u7iHX8enDo7UmCo3i5vg"
    "9Kk/ZvO/u0PLVA=="
)
