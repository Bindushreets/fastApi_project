'''--------------------------------------------'''
        # CRUD App with FastAPI
'''--------------------------------------------'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import pandas as pd
import json
from datetime import datetime

# Read the excel through pandas.
df = pd.read_excel("Articles.xlsx")

# Define the Model : 

app = FastAPI()
excel_path = "Articles.xlsx"


class ArticlesData(BaseModel):
    Article_Id : int
    Article_Date : str
    Category : str
    Article_Name : str 
    Article_Content : str

#---------------------------------------------------------------------------------------

1.  #  Implement CREATE Operation : 

articles_list = []                      # In-memory list to store articles temporarily

@app.post("/ArticlesCreate")
def create_article(article: ArticlesData):

    # Add the new article to the list
    articles_list.append(article.dict())

    # Convert to DataFrame
    df_new = pd.DataFrame(articles_list)

    # Save back to Excel (overwrites each time for simplicity)
    df_new.to_excel(excel_path, index=True)
    return {"message": "Article added successfully", "article": article}

#------------------------------------------------------------------------------------------------

2.  # Implement READ Operation : 

'''    2.1  # To get all Articles : '''

@app.get("/ArticlesRead")
def read_articles():
    return json.loads(df.to_json(orient="records"))

''''    2.2 # To get a Article by its ID : '''

@app.get("/articles/{Article_Id}")
def get_articles(article_id: Optional[int]):
        filtered_df = df[df["Article_Id"] == article_id]
        return json.loads(filtered_df[["Article_Id", "Article_Name"]].to_json(orient="records"))

#----------------------------------------------------------------------------------------------------

3. # Implement UPDATE Operation :

'''     3.1 # Update the entire data in the row : '''

@app.put("/ArticlesUpdate")
def update_article(article: ArticlesData):
    try:
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Excel file not found")

    # Find row where Article_Id matches
    match_index = df.index[df["Article_Id"] == article.Article_Id].tolist()

    if not match_index:
        raise HTTPException(status_code=404, detail="Article ID not found")

    # Update the row
    id = match_index[0]
    df.loc[id, "Article_Date"] = article.Article_Date
    df.loc[id, "Category"] = article.Category
    df.loc[id, "Article_Name"] = article.Article_Name
    df.loc[id, "Article_Content"] = article.Article_Content

    # Save back to Excel
    df.to_excel(excel_path, index=False)

    return {"message": "Article updated successfully", "updated_article": article}

'''     3.2 # Update the partial data in the row : '''

@app.patch("/ArticlesPatch")
def patch_article(update_data: ArticlesData):

    # Find the row index :
    id_list = df.index[df["Article_Id"] == update_data.Article_Id].tolist()
    if not id_list:
        raise HTTPException(status_code=404, detail="Article ID not found")
    
    id = id_list[0]

    # Only update the fields that were provided
    for field, value in update_data.dict(exclude_unset=True).items():
        if field != "Article_Id" and value not in ["string", "", None]:
            df.at[id, field] = value

    # Save updated data
    df.to_excel(excel_path, index=False)

    # Get the full updated row 
    updated_row = df.loc[id].to_dict()
    print("Update data:", update_data.dict())
    print("DataFrame columns:", df.columns.tolist())
    return {"message": "Article partially updated", "updated_fields": updated_row}

#----------------------------------------------------------------------------------------------------

4. # Implement DELETE Operation :

@app.delete("/ArticlesDelete/{Article_Id}")
def delete_article(Article_Id: int):
    # Find the row index
    id_list = df.index[df["Article_Id"] == Article_Id].tolist()
    
    if not id_list:
        raise HTTPException(status_code=404, detail="Article ID not found")
    
    # Drop the row
    df.drop(index=id_list[0], inplace=True)
    
    # Save updated data
    df.to_excel(excel_path, index=False)
    
    return {"message": f"Article with ID {Article_Id} has been deleted."}

#----------------------------------------------------------------------------------------------------