from fastapi import FastAPI, Header, Query, status, HTTPException, Body
from typing import List
from pydantic import BaseModel, Field
import pandas as pd
from decouple import Config, RepositoryEnv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import tensorflow as tf
import os
from ml import alpha
import datetime

from api.schema import (
    Recipe_User_Profile,
    Recipe_Req_Body,
    SMW_Req_Body,
    SMW_USER_PROFILE,
)
from utils.user_recipe_profile import generate_user_profile_for_recipe
from utils.smw_user_profile import create_smw_user_profile
from utils.supabase import recipe_table, article_table, session_table
from sre.recipe import recommend_recipes
from sre.recommender import Recommender

app = FastAPI()

env = Config(RepositoryEnv(".env"))
X_API_KEY = env.get("SRE_INTERNAL_KEY")


async def check_secret_key(api_key: str = Header(...)):
    if api_key != X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req, exc):
    print(exc)
    error_fields = [error["loc"][0] for error in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Missing required fields: {', '.join(error_fields)}"},
    )


@app.get("/")
async def root():
    return {"msg": "hello world", "status": 200}


@app.post("/v1/sre/recipes")
async def v1_recommend_recipe(
    body: Recipe_Req_Body, x_api_key: str = Header(..., alias="x-api-key")
):
    await check_secret_key(x_api_key)
    user_profile = Recipe_User_Profile(**body.dict())
    user_profile = user_profile.dict()
    profile = generate_user_profile_for_recipe(user_profile)
    resp = recipe_table.select("*").execute()
    recipes = pd.DataFrame(resp.data)
    recommended_recipes = recommend_recipes(profile, recipes)
    recommended_recipes_dict = recommended_recipes.to_dict(orient="records")
    return JSONResponse(recommended_recipes_dict, status_code=status.HTTP_200_OK)


@app.post("/v1/sre/sessions")
async def v1_recommend_sessions(
    body: SMW_Req_Body, x_api_key: str = Header(..., alias="x-api-key")
):
    await check_secret_key(x_api_key)
    # Your logic for sessions recommendation
    input = SMW_USER_PROFILE(**body.dict())
    user_profile = create_smw_user_profile(input.dict())
    # todo: cache labels for like an hour or 2 to improve API performance
    model = tf.keras.models.load_model("models/aplha_model.keras")
    path_to_save = os.path.join("data", "fitness-dataset.csv")
    df = pd.read_csv(path_to_save)
    features, labels, label_encoder, ohe = alpha.preprocess_data(df)
    input_df = pd.DataFrame(user_profile)
    input_features = alpha.preprocess_input_data(input_df, label_encoder, features)

    predictions = model.predict(input_features)
    labels = []
    for pred in zip(alpha.fitness_categories, predictions[0]):
        label, score = pred
        labels.append(label)

    # use sre to make session booking recommendation for users
    current_time = datetime.datetime.now()
    one_hour_ahead = current_time + datetime.timedelta(hours=1)
    today_start = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    today_end = datetime.datetime.now().replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    response = (
        session_table.select("*")
        .gte("startTime", today_start.strftime("%Y-%m-%dT%H:%M:%S"))
        .lte("endTime", today_end.strftime("%Y-%m-%dT23:59:59"))
        .gte("startTime", one_hour_ahead.strftime("%Y-%m-%dT%H:%M:%S"))
        .execute()
    )
    sessions = pd.DataFrame(response.data)
    recommender = Recommender(sessions)
    recommendations = recommender.get_recommendations(label)
    return JSONResponse(recommendations.to_dict(orient='records'), status_code=status.HTTP_200_OK)


@app.get("/v1/sre/articles")
async def v1_recommend_articles(
    tags: List[str] = Query(...), x_api_key: str = Header(..., alias="x-api-key")
):
    await check_secret_key(x_api_key)
    articles_query = article_table.select("*").execute()
    articles = pd.DataFrame(articles_query.data)
    recommender = Recommender(articles)
    recommendations = recommender.get_recommendations(tags)
    return JSONResponse(
        recommendations.to_dict(orient="records"), status_code=status.HTTP_200_OK
    )
