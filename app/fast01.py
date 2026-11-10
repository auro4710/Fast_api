from re import search

from click.testing import Result
from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn
from pygments.lexer import default
from pydantic import BaseModel,Field
from decimal import Decimal
from datetime import datetime, timedelta, timezone

from models import User
app = FastAPI()

from book import book1
app.include_router(book1, prefix="/book")

from fastapi import Request

from pathlib import Path

from fastapi.staticfiles import StaticFiles

# 以文件位置为基准，避免依赖启动时的工作目录
BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

from fastapi.templating import Jinja2Templates

template = Jinja2Templates(directory=str(BASE_DIR / "templates"))

from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    add_exception_handlers=True,
)

categories = [
    {"id": 1, "name": "饮料", "create_time": "2026-10-13 08:00:00"},
    {"id": 2, "name": "数码配件", "create_time": "2026-10-13 08:00:00"},
    {"id": 3, "name": "零食", "create_time": "2026-10-13 08:00:00"},
]

products = [
    {
        "id": 1,
        "category_id": 1,
        "name": "矿泉水",
        "price": "3.50",
        "stock": 100,
        "shelf_status": True,
        "create_time": "2026-10-13 09:00:00",
    },
    {
        "id": 2,
        "category_id": 1,
        "name": "可乐",
        "price": "5.00",
        "stock": 80,
        "shelf_status": True,
        "create_time": "2026-10-13 10:00:00",
    },
    {
        "id": 3,
        "category_id": 2,
        "name": "USB 数据线",
        "price": "19.90",
        "stock": 0,
        "shelf_status": False,
        "create_time": "2026-10-13 11:00:00",
    },
]

class ProductCreate(BaseModel):
    """新增商品客户端可以提交的字段"""
    category_id: int = Field(gt=0, description="商品分类的ID，必须是正整数")
    name: str = Field(
        min_length=1, max_length=50, description="商品名称，必填，不超过50个字符"
    )
    price: Decimal = Field(
        ge=0, decimal_places=2, max_digits=8, description="商品价格，最大保留2位小数"
    )
    stock: int = Field(default=0, ge=0, description="库存，不小于0")
    shelf_status: bool = Field(default=True, description="上架状态")

class ProductUpdate(BaseModel):
    """修改商品 客户端可以提交的字段 局部修改"""

    category_id: int | None = Field(
        default=None, gt=0, description="商品分类的ID，必须是正整数"
    )
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="商品名称，必填，不超过50个字符",
    )
    price: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
        max_digits=8,
        description="商品价格，最大保留2位小数",
    )
    stock: int | None = Field(default=None, ge=0, description="库存，不小于0")
    shelf_status: bool | None = Field(default=None, description="上架状态")

import fastapi_cdn_host
fastapi_cdn_host.patch_docs(app)
# @app.get("/")
# async def get_test(request: Request):
#     # print(request.query_params.get("name"))
#     # return {"message": "Hello World"}
#     return template.TemplateResponse(request, "1.html")
@app.post("/")
async def post_test(request: Request):
    result = await request.json()
    name = result["name"]
    age = result["age"]
    await User.create(name=name, age=age)
    return {"message": "Hello World"}

@app.put("/{user_id}")
async def put_test(request: Request, user_id: int):
    result = await request.json()
    name = result["name"]
    age = result["age"]
    await User.filter(id=user_id).update(name=name, age=age)
    return {"message": "Hello World"}
@app.delete("/{user_id}")
async def delete_test(request: Request, user_id: int):
    result = await request.json()
    name = result["name"]
    await User.filter(id=user_id).delete()

@app.get("/")
async def get_users(request: Request):
    user = await User.get(id=3)
    print(user)

    users = await User.all()
    print(users)

def get_product_or_404(product_id: int):
    """按 ID 返回商品字典，不存在时抛出 404。"""
    product = next((item for item in products if item["id"] == product_id), None)
    # 未找到匹配记录时返回 404，让查询、修改和删除使用同一规则。
    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@app.get("/products/{product_id}")
async def read_product(request: Request, product_id: int = Path(gt=0)):
    """接受商品id返回商品信息，否则返回Nnoe"""
    return get_product_or_404(product_id)

@app.get("/products")
async def list_products(keyword : str|None = Query(default=None, max_length=50),
                        page: int = Query(default = 1, ge=1),
                        page_size: int = Query(default = 2,ge=1, le=100)):
    """"接受页码和每页条数，返回商品列表和商品总数"""
    filter_products = products
    if keyword and keyword.strip():
        search_text = keyword.strip().lower()
        filter_products = []
        for porduct in products:
            if porduct["name"].lower() == search_text:
                filter_products.append(porduct)

    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": filter_products[start:end],
        "total": len(filter_products),
        "page": page,
        "page_size": page_size,
    }

@app.post("/products")
async def create_product(payload: ProductCreate):
    """接收商品新增的数据，暂时先返回校验后数据"""
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="商品名称不能为空")
    if not any(payload.category_id == category["id"] for category in categories):
        raise HTTPException(status_code=400, detail="分类ID不存在")
    payload.name = name
    # 新增商品  我们需要从商品列表里找到最大的ID  再 +1 变成新的商品ID
    next_id = max((product["id"] for product in products), default=0) + 1
    payload.model_dump()
    # **dict 放到了 ProductCreate(**dict) -> name="矿泉水", price=2.23
    # **{"name": "矿泉水"} -> {"name": "矿泉水"}
    product = {
        "id": next_id,
        **payload.model_dump(),
        "create_time": datetime.now(timezone(timedelta(hours=8))).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }  # UTC +8
    products.append(product)
    return product

@app.patch("/products/{product_id}")
async def update_product(payload: ProductUpdate, product_id: int = Path(gt=0)):
    """接收商品修改字段的数据，更新对应的商品字段数据  返回修改后的商品数据"""
    # 确认商品是否存在
    product = get_product_or_404(product_id)
    # 看下本次提交的数据有无新增的字段需要改动
    changes = payload.model_dump(exclude_unset=True)  # {"name": null} -> {}
    if not changes:
        raise HTTPException(status_code=400, detail="至少提交一个需要修改的字段")

    for field, value in changes.items():
        if value is None:
            # 判断客户端是否提交了 值为None 的字段
            raise HTTPException(
                status_code=400, detail=f"字段 {field} 的值不允许为 null"
            )
    if "name" in changes:
        changes["name"] = changes["name"].strip()  # ""
        if not changes["name"]:
            raise HTTPException(status_code=400, detail="商品名称不能为空")
    if "category_id" in changes:
        if not any(category["id"] == changes["category_id"] for category in categories):
            raise HTTPException(status_code=400, detail="商品分类不存在")
    product.update(changes)  # 按照 key 来进行覆盖  {"name": "巧克力", "stock" : 100}
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int = Path(gt=0)):
    """根据商品ID删除商品"""
    product = get_product_or_404(product_id)
    products.remove(product)
    return {"message": "商品删除成功"}

if __name__ == '__main__':
    uvicorn.run(app)