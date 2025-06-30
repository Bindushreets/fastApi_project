# 📰 API with FastAPI & Pandas

This FastAPI project provides a RESTful API for 
retrieving, filtering, and managing article data from an Excel file using pandas. 
It includes support for date filtering, category matching, content search, and dynamic response formatting.

## 📁 Project Structure

- `Articles.xlsx`: Excel file containing article data.
- `main.py`: FastAPI app with multiple endpoints.
- `pydantic` models for input validation.
- Endpoints with `GET`, `POST`, and `DELETE` methods.
- Dynamic date formatting using Unix timestamp conversion.

## 🚀 How to Run

```bash
pip install fastapi[all] pandas openpyxl
uvicorn main:app --reload
fastapi dev python main.py
```

## 📌 Endpoints

### Root
- **`GET /`**  
  Returns a welcome message.

### Retrieve All Articles
- **`GET /Articles`**  
  Lists all articles with ID and Name.

### Retrieve by Article ID
- **`POST /id/`**  
  Filters article content by `Article_Id`.

### Filter by Date & Category (AND)
- **`POST /dateandcategory/`**  
  Returns article matching both date and category.

### Filter by Date OR Category
- **`POST /dateorcategory/`**  
  Returns articles matching either date or category.

### Fix Date Format (AND)
- **`POST /datefixand/`**  
  Converts Unix timestamp to `dd-mm-yyyy` format.

### Fix Date Format (OR)
- **`POST /datefixor/`**  
  Same as above, but for OR condition.

### List Comprehension Formatters
- **`POST /datefixLCusingand/`**  
- **`POST /datefixLCusingor/`**  
  Date fix with list comprehension and performance boost.

### Response with Status Code
- **`POST /name/`**  
  Looks up by `Article_Name` and returns structured JSON with status codes.

### Query Parameter Example
- **`GET /ArticleGqp?article_id=1`**  
  Filters using query parameter.

### Read Full Excel
- **`GET /read/`**  
  Returns all articles.

### Delete by ID
- **`DELETE /delete/{Article_Id}`**  
  Removes an article by ID and updates the Excel file.

## 🧠 Features

- Excel integration with `pandas`
- Dynamic data filtering
- JSON conversion with status codes
- Date formatting from Unix timestamps
- Clean error handling with `HTTPException` & `JSONResponse`

## 📦 Dependencies

- `fastapi`
- `pydantic`
- `pandas`
- `openpyxl` (for Excel reading)
