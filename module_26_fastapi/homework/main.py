from typing import List, Optional

from fastapi import FastAPI
from sqlalchemy.future import select

import models
import schemas
from database import engine, session

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get('/recipe/', response_model=List[schemas.RecipeShortModel])
async def recipes() -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe))
    return res.scalars().all()


@app.post('/recipe/{idx}', response_model=schemas.RecipeModel)
async def recipe(idx: Optional[int] = None) -> List[models.Recipe]:
    recipe = await session.execute(select(models.Recipe).where(models.Recipe.id == idx))
    recipe = recipe.scalars().one()
    recipe.view_count += 1
    await session.commit()
    return recipe
