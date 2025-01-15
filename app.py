from blog_backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # 개발 모드에서 실행