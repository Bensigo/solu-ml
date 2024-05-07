from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, Query, status, HTTPException, Body
from typing import List
from pydantic import BaseModel, Field
import pandas as pd
from decouple import Config, RepositoryEnv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import tensorflow as tf
from supabase import create_client, Client
from supabase.client import ClientOptions
import os
import datetime

from app.api.schema import (
    Recipe_User_Profile,
    Recipe_Req_Body,
    SMW_Req_Body,
    SMW_USER_PROFILE,
)
from app.ml import alpha
from app.ml.alpha import __VERSION__ as AI_MODEL_VERSION
from app.utils.user_recipe_profile import generate_user_profile_for_recipe
from app.utils.smw_user_profile import create_smw_user_profile
from app.sre.recipe import recommend_recipes
from app.sre.recommender import Recommender



# env = Config(RepositoryEnv(".env"))
# X_API_KEY = env.get("SRE_INTERNAL_KEY")
X_API_KEY = os.getenv("SRE_INTERNAL_KEY")

model = {}

# url: str = env.get("SUPABASE_URL")
# key: str = env.get("SUPABASE_KEY")


url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

table = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # run on start server
    supabase: Client = create_client(
        url,
        key,
        options=ClientOptions(postgrest_client_timeout=10, storage_client_timeout=10),
    )
    table["Recipe"] = supabase.table("Recipe")
    table["Resource"] = supabase.table("Resource")
    table["Session"] = supabase.table("Session")

    model["alpha"] = tf.keras.models.load_model(f"app/models/aplha_model_{AI_MODEL_VERSION}.keras")
    yield
    # run after the app  has finished
    model.clear()


app = FastAPI(lifespan=lifespan)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req, exc):
    print(exc)
    error_fields = [error["loc"][0] for error in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Missing required fields: {', '.join(error_fields)}"},
    )


async def check_secret_key(api_key: str = Header(...)):
    if api_key != X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )



@app.get("/")
async def root():
    return { "status": "alive", "health_check": "OK", "model_version": AI_MODEL_VERSION}


@app.post("/v1/sre/recipes")
async def v1_recommend_recipe(
    body: Recipe_Req_Body, x_api_key: str = Header(..., alias="x-api-key")
):
    await check_secret_key(x_api_key)
    user_profile = Recipe_User_Profile(**body.dict())
    user_profile = user_profile.dict()
    profile = generate_user_profile_for_recipe(user_profile)
    resp = table["Recipe"].select("*").execute()
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
    # model = tf.keras.models.load_model("models/aplha_model.keras")
    path_to_save = os.path.join("data", "fitness-dataset.csv")
    df = pd.read_csv(path_to_save)
    features, labels, label_encoder, ohe = alpha.preprocess_data(df)
    input_df = pd.DataFrame(user_profile)
    input_features = alpha.preprocess_input_data(input_df, label_encoder, features)

    predictions = model["alpha"].predict(input_features)
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
        table["Session"].select("*")
        .gte("startTime", today_start.strftime("%Y-%m-%dT%H:%M:%S"))
        .lte("endTime", today_end.strftime("%Y-%m-%dT23:59:59"))
        .gte("startTime", one_hour_ahead.strftime("%Y-%m-%dT%H:%M:%S"))
        .execute()
    )
    sessions = pd.DataFrame(response.data)
    recommender = Recommender(sessions)
    recommendations = recommender.get_recommendations(label)
    if recommendations is None:
        return JSONResponse([], status_code=status.HTTP_200_OK)
    return JSONResponse(
        recommendations.to_dict(orient="records"), status_code=status.HTTP_200_OK
    )





@app.get("/v1/sre/articles")
async def v1_recommend_articles(
    tags: List[str] = Query(...), x_api_key: str = Header(..., alias="x-api-key")
):
    await check_secret_key(x_api_key)
    articles_query = table["Resource"].select("*").execute()
    articles = pd.DataFrame(articles_query.data)
    recommender = Recommender(articles)
    recommendations = recommender.get_recommendations(tags)
    return JSONResponse(
        recommendations.to_dict(orient="records"), status_code=status.HTTP_200_OK
    )
