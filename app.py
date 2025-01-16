from blog_backend import create_app
from flask_cors import CORS

app = create_app()
CORS(app, resources={
r"/v1/*": {"origin": "*"},
r"/api/*": {"origin": "*"},
})
if __name__ == '__main__':
    app.run(port=3308)  # 개발 모드에서 실행