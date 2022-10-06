import psycopg2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

database = psycopg2.connect(host='localhost',
                            dbname='postgres',
                            user='postgres',
                            password='p5ssw0rd',
                            port=5432)

cursor = database.cursor()


@app.get("/")
async def root():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Exam Classroom</title>
        </head>
        <body>
        
        <script>
            function doSomething() {
                // alert(document.forms[0].elements['name'].value);
                var url = document.forms[0].elements['name'].value;
                window.location = url;
                return false;
            }
        </script>
        
        <form onsubmit="return doSomething();" class="my-form">
            <input type="text" name="name">
            <input type="submit" value="조회하기">
        </form>
        
        
        </body>
        </html>
        """
    )


@app.get("/{code}")
async def ret(code: str):
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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
