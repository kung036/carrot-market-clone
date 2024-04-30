from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
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

# 토큰 발급
SECRET = "super-coding" # 인코딩키
manager = LoginManager(SECRET, '/login')

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
async def get_items(user=Depends(manager)): # 인증된 상태에만 허용
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
    return Response(content=bytes.fromhex(image_bytes), media_type='image/*') # 16진법 해석 후 바이트 변환해서 반환

# 회원가입한 정보 찾기
@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''name="{data["name"]}"'''
    
    con.row_factory = sqlite3.Row # 컬럼명을 가져옴
    cur = con.cursor()

    user = cur.execute(f"""
                       SELECT * FROM users
                       WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

# 로그인
@app.post('/login')
def login (id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_user(id)
    print(user)
    
    # 로그인 실패 시 에러 처리
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    # access token 발급
    access_token = manager.create_access_token(data={
        'sub' : {
            'id':user['id'],
            'name':user['name'],
            'email':user['email']            
        }
    })
    
    return {'access_token':access_token}

# 회원가입
@app.post('/signup')
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()],
           ):
    # 회원가입 중복방지 코드 추가하기(에러 발생)
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES('{id}','{name}','{email}','{password}');
                """)
    con.commit()
    return 200

# root 경로(위에 api 작성해야 적용됨)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
