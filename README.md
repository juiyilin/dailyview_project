# 此專案使用 docker-compose 執行，作業系統為 Ubuntu
使用 Nginx + uWSGI + Python 3.7 + Django 3.2 (Django REST framework 3.13.1) + PostgreSQL 12 + redis
## 下載專案  
`git clone https://github.com/juiyilin/dailyview_project.git`

下載完在專案資料夾與 docker-compose.yml 同級目錄下新增.env檔案  
內容須包含

    POSTGRESQL_NAME = <自訂資料庫名稱>
    POSTGRESQL_USER = <自訂資料庫帳號>
    POSTGRESQL_PASSWORD = <自訂資料庫密碼>
    POSTGRESQL_HOST = db
    POSTGRESQL_PORT = 5432
    REDIS_DEFAULT = cache
    SUPER = <自訂 API 登入帳號>
    SUPER_PASSWORD = <自訂 API 登入密碼>

啟動專案 `sudo docker-compose up`  
停止專案 `sudo docker-compose down`  

待 terminal 出現類似   

    WSGI app 0 (mountpoint='') ready in 1 seconds on interpreter 0x55a5b17aaeb0 pid: 2035203 (default app)
    mountpoint  already configured. skip.
    
表示成功啟動

瀏覽器輸入 [http://0.0.0.0:8001/docs/](http://0.0.0.0:8001/docs/) 可以看到測試 API 的 Swagger 頁面


## API 介紹
**API 分為兩大類**
1. 使用者登入相關
2. 文章相關

**使用者登入相關 API 如下:**  

- 登入 `POST /api/jwt_login/`  
登入的 username 與 password 請分別輸入 .env 中 SUPER 與 SUPER_PASSWORD 的內容。  
登入成功後拿到的 access 為 access token 用於做身分驗證；refresh 為 refresh token 用於登出(/api/jwt_logout/)與拿取新的 access token (/api/refresh/)  
access token 與 refresh token 的效期分別為 5 分鐘與 1 小時
- 拿取新的 access token `POST /api/refresh/`
當 access token 過期時 refresh 輸入登入 API 中拿到的 refresh 的值，可以換取新的 access token

- 登出 `POST /api/jwt_logout/`
refresh 輸入登入 API 中拿到的 refresh 的值會存入資料庫的黑名單表，並且會將 header 中的 access token 存入 redis 中保存 5 分鐘


**文章相關 API 如下:**  

- 取得熱門文章 `GET /api/article/`  
對應 DailyView 網頁的位置  
![](./static/readme/famous.png)  
可傳參數：  
頁數 page  
每頁筆數 size  
是否回傳熱門文章 famous (此專案熱門文章的定義為點擊數 >= 5)  
famous 為 1 回傳熱門文章，其他值或不傳此參數將回傳所有文章並按照發佈時間新->舊排序；若 famous 為 1，但沒有點擊數 >= 5 的文章，將會回傳所有文章並按照發佈時間新->舊排序  

回傳格式如下
```python
# 所有 image 欄位需再加上 http://0.0.0.0:8001/ 組合成完整圖片網址
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "一二三",
      "publish_date": "2023-09-02",
      "small_image": "/static/uploads/article/2c9b5717d07347ecae48538f112e7315/s-1693664963-擷取.PNG"
    }
  ]
}
```

#### 文章新增、修改 API 考慮到會有各別編輯段落或區塊的需求，所以拆分成新增、修改大標題與大綱 和 新增、修改段落或區塊
- 新增大標題與大綱 `POST /api/article/`  
須傳入參數：  
標題 title  
大綱(摘要) summary  
大圖 main_image  
小圖 small_image  
標籤 tag  (已預先建立)  
```python
# 所有標籤
tag = {
    1: '熱門', 2: '時事', 3: '政治', 4: '娛樂', 5: '網紅', 
    6: '生活', 7: '美食', 8: '旅遊', 9: '兩性', 10: '寵物', 
    11: 'ACG', 12: '產經', 13: '運動'
}
```

- 修改大標題與大綱 `PUT /api/article/<str:pk>/`  
pk 為 `GET /api/article/` 或 `POST /api/article/` 回傳的 id  
須傳入參數與 `POST /api/article/` 相同  


- 新增段落(區塊)內文 `POST /api/article/<str:article_id>/detail/`  
article_id 為 `GET /api/article/` 或  `POST /api/article/` 回傳的 id  
傳入參數
第幾段落(區塊) block  
段落(區塊)標題 title  
段落(區塊)內容 content  
段落(區塊)附圖 image  

- 取得單一文章完整內容 `GET /api/article/<str:article_id>/detail/`  
***每 GET 一次都會視為一次點擊***  

回傳格式如下
```python 
{
  "id": 1,
  "detail": [
    {
      "id": 1,
      "block": 1,
      "title": "1111111",
      "content": "111111111111",
      "image": null
    }
  ],
  "title": "一二三",
  "summary": "一一一一一二二二",
  "small_image": "/static/uploads/article/2c9b5717d07347ecae48538f112e7315/s-1693664963-擷取.PNG",
  "main_image": "/static/uploads/article/2c9b5717d07347ecae48538f112e7315/m-1693664963-擷取.PNG",
  "publish_date": "2023-09-02",
  "tag": "熱門",
  "click": 1
}
```
detail 中為各段落(區塊)的內文資料

- 修改段落(區塊)內文 `PUT /api/article/detail/<str:pk>/`  
pk 為 `GET /article/{article_id}/detail/` 回傳的 detail 中的 id  
需傳參數與 `POST /api/article/<str:article_id>/detail/` 相同  
若 image 不修改不用傳此參數

- 刪除段落(區塊)內文 `DELETE /api/article/detail/<str:pk>/`  
pk 為 `GET /article/{article_id}/detail/` 回傳的 detail 中的 id  

- 刪除整篇文章 `DELETE /api/article/<str:pk>/`  
pk 為 `GET /api/article/` 或 `POST /api/article/` 回傳的 id  
