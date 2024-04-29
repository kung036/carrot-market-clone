from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()


# deta.space에 테이블 생성하기 위함(백엔드 코드 실행 시 테이블 생성)
# IF NOT EXISTS : 없을 때만 테이블 생성
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
            );
            """)

app = FastAPI()

# 하향식 코드
# item 생성
@app.post("/item")
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    # 받은 데이터를 DB에 넣기
    image_bytes = await image.read() # 이미지를 읽는 시간 필요
    cur.execute(f"""
        INSERT INTO items(title,image,price,description,place,insertAt)
        VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})
    """)
    con.commit()
    return '201'
    

# item 조회
@app.get('/items')
async def read_items():
    con.row_factory = sqlite3.Row # 컬럼명을 가져옴
    cur = con.cursor()
    rows = cur.execute(f"""
        SELECT * from items;
    """).fetchall()
    response = JSONResponse(jsonable_encoder(dict(row) for row in rows))
    return response

# 이미지 요청
@app.get('/image/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
        SELECT image FROM items WHERE id={item_id}
    """).fetchone()[0] # hex(16진법)
    return Response(content=bytes.fromhex(image_bytes)) # 16진법 해석 후 바이트 변환해서 반환

# root 경로(위에 api 작성해야 적용됨)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
