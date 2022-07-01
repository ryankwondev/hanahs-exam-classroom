from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psycopg2
import json

app = FastAPI()

database = psycopg2.connect(host='postgres',
                            dbname='postgres',
                            user='postgres',
                            password='p5ssw0rd',
                            port=5432)

cursor = database.cursor()


@app.get("/{code}")
async def root(code: str):
    try:
        cursor.execute(
            f"SELECT * FROM examroom WHERE code = '{code}';"
        )

        result = f"<h3>조회번호: {code}</h3>\n"
        result += "<p>=========================</p>\n"

        for i in cursor.fetchall():
            (code, subject, date, period, room) = i
            result += f"<p>{date} {period}교시 | {room} | {subject}</p>\n"
            result += "<p>=========================</p>\n"

        result += "<p>본 페이지는 참고용으로만 이용해주세요.</p>\n"

        return HTMLResponse(result)

    except Exception as e:
        return {"error": str(e)}
