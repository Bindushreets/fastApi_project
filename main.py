from typing import Union, Optional

from fastapi import FastAPI , status , HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel

import os
import pandas as pd
import json
from datetime import datetime


df = pd.read_excel("Articles.xlsx")
# print(df.head(2))

app = FastAPI()
excel_path = "Articles.xlsx"



class Articles(BaseModel):
    Article_Id : int


class ArticleName(BaseModel):
    Article_Name : str


class ArticleDateCategory(BaseModel):
    Article_Date : str
    Category : str    


class ArticlesData(BaseModel):
    Article_Id : int
    Article_Date : str
    Category : str
    Article_Name : str 
    Article_Content : str


# landing Screen : http://127.0.0.1:8000/
@app.get("/")
def read_root():
    return {"Hello": "Bindu"}

# get method : http://127.0.0.1:8000/Articles
@app.get("/Articles")
def Articleslist_Get_Method():
    return json.loads (df[["Article_Id","Article_Name"]].to_json(orient="records"))


# post method : http://127.0.0.1:8000/id/
@app.post("/id/")
def Article_Post_Method(Id: Articles):
  filter_articlesContent =  json.loads(df[df['Article_Id'] == Id.Article_Id].to_json(orient="records"))
  return {"Article Id " : filter_articlesContent[0].get("Article_Id"),
          "Articles Content through Article Id" : filter_articlesContent[0].get("Article_Content")
          }

# post method : AND operation : http://127.0.0.1:8000/dateandcategory/ 
@app.post("/dateandcategory/")
def Article_date_and_category(DateCategory: ArticleDateCategory):
  filter_articles =  json.loads(df[(df['Article_Date'] == DateCategory.Article_Date) & 
                                   (df['Category'] == DateCategory.Category)].to_json(orient="records"))
  return {"Article Id" : filter_articles[0].get("Article_Id"),
          "Article Date" : filter_articles[0].get("Article_Date"),
          "Articles Content" : filter_articles[0].get("Article_Content") 
          }

# post method : OR operation : http://127.0.0.1:8000/dateorcategory/
@app.post("/dateorcategory/")
def Article_date_or_category(Date_or_Category: ArticleDateCategory):
  filter_articles =  (df[(df['Article_Date'] == Date_or_Category.Article_Date) | 
                                   (df['Category'] == Date_or_Category.Category)].to_json(orient="records"))
  return json.loads(filter_articles)

# post method : fix the date format : http://127.0.0.1:8000/datefixand/
@app.post("/datefixand/")
def Article_date_and_category_fix(DateCategory_and: ArticleDateCategory):
  filter_articles =  json.loads(df[(df['Article_Date'] == DateCategory_and.Article_Date) & 
                                   (df['Category'] == DateCategory_and.Category)].to_json(orient="records"))
  for i in filter_articles:
     i["Article_Date"] = ((datetime.fromtimestamp((i.get("Article_Date")) / 1000)).strftime("%d-%m-%Y"))
     return  json.loads(json.dumps(filter_articles))
     
# post method : fix the date format : http://127.0.0.1:8000/datefixor/
# Need to resolve........! logic is working only for 1st set of data.
@app.post("/datefixor/")
def Article_date_or_category_fix(DateCategoryfix: ArticleDateCategory):
  filter_articles =  json.loads(df[(df['Article_Date'] == DateCategoryfix.Article_Date) |
                                   (df['Category'] == DateCategoryfix.Category)].to_json(orient="records"))
  for i in filter_articles:
    # date_str = i.get("Article_Date")
    # date = datetime.fromtimestamp(date) / 1000)
    # formatted_date = date.strftime("%d-%m-%Y"))
    # i["Article_Date"] = formatted_date
    i["Article_Date"] = ((datetime.fromtimestamp((i.get("Article_Date")) / 1000)).strftime("%d-%m-%Y"))
    return  {"output" : json.loads(json.dumps(filter_articles))}
  
# post method : fix the date format with List Comprhension method : http://127.0.0.1:8000/datefixLCusingand/
@app.post("/datefixLCusingand/")
def Article_date_and_category_lc(Date_Category: ArticleDateCategory):
    filter_articles = df[(df['Article_Date'] == Date_Category.Article_Date) & (df['Category'] == Date_Category.Category)].to_json(orient='records')
    parsed_list = json.loads(json.dumps([{**item, "Article_Date": datetime.fromtimestamp(item["Article_Date"] / 1000).strftime("%d-%m-%Y")}for item in json.loads(filter_articles)]))
    return parsed_list

# post method : fix the date format with List Comprhension method : http://127.0.0.1:8000/datefixLCusingor/
@app.post("/datefixLCusingor/")
def Article_date_or_category_lc(DateCategoryfixlc: ArticleDateCategory):
  filter_articles =  df[(df['Article_Date'] == DateCategoryfixlc.Article_Date) | (df['Category'] == DateCategoryfixlc.Category)].to_json(orient="records")
  parsed_list = json.loads(json.dumps([{**item, "Article_Date": datetime.fromtimestamp(item["Article_Date"] / 1000).strftime("%d-%m-%Y")}for item in json.loads(filter_articles)]))
  return parsed_list

# post method : adding the status code and message using Exception handling with JSONResponse : http://127.0.0.1:8000/name/
@app.post("/name/")
def Article_Post_Method(A_Name: ArticleName):
  try:
      filter_articlesContent =  json.loads(df[df['Article_Name'] == A_Name.Article_Name].to_json(orient="records"))
      return JSONResponse(status_code = status.HTTP_200_OK,
                          content = {"status": "Success", "message": "Item processed",
                                     "Article Name" : filter_articlesContent[0].get("Article_Name"),
                                     "Articles Content" : filter_articlesContent[0].get("Article_Content")
                                     }
                                     )
  except Exception as e:
      return JSONResponse(status_code = status.HTTP_404_NOT_FOUND,
            content = {"status": "failed", "message": str(e)}
        )
  
# get query method : http://127.0.0.1:8000/ArticleGqp?article_id=1
@app.get("/ArticleGqp")
def get_articles(article_id: Optional[int]):
        filtered_df = df[df["Article_Id"] == article_id]
        return json.loads(filtered_df[["Article_Id", "Article_Name"]].to_json(orient="records"))


# read the Excel : http://127.0.0.1:8000/read/
@app.get("/read/")
def read_excel():
    return json.loads(df.to_json(orient="records"))


# DELETE : 
@app.delete("/delete/{Article_Id}")
def delete_article(Article_Id: int):
    
    excel_path = "Articles.xlsx"
    df = pd.read_excel("Articles.xlsx")

    if Article_Id not in df["Article_Id"].values:
        return JSONResponse(status_code = 404, content = {"Details": "Article not found"})
    
    df_data = df[df["Article_Id"] != Article_Id]

    df_data.to_excel(excel_path, index=False)
    return {"message": f"Article with ID {Article_Id} is deleted now"}