from pydantic import BaseModel


class BaseRecipe(BaseModel):
    id: int
    name: str
    cooking_time: int
    ingredient_list: str
    description: str
    view_count: int


class RecipeShortModel(BaseRecipe):
    id: int
    name: str
    view_count: int
    cooking_time: int

    class Config:
        orm_mode = True

    ...


class RecipeModel(BaseRecipe):
    id: int
    name: str
    cooking_time: int
    ingredient_list: str
    description: str

    class Config:
        orm_mode = True
