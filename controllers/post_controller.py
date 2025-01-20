from flask_restx import Namespace, Resource
from flask import jsonify, request
# from blog_backend import db
from dotenv import load_dotenv
import os
import pymysql
import blog_backend.services.main_service as main_service

# .env 파일 auto load
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = os.getenv('DB_NAME')

db = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
ROUTER = Namespace(name='Main Api들', path='/', description='This api is posts')
cursor = db.cursor()

db.ping(reconnect=True)
def get_db_connection():
    """데이터베이스 연결을 생성하고 반환하는 함수"""
    return pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')

@ROUTER.route('/posts')
@ROUTER.doc(params={'category': '파라미터로 입력된 카테고리'})
@ROUTER.doc(params={'searchText': '파라미터로 입력된 검색어'})
@ROUTER.header('content-type', 'application/json')
class PostRoute(Resource):
    def get(self) -> str:
        """포스트 조회"""
        db = get_db_connection()  # 데이터베이스 연결 생성
        cursor = db.cursor()  # 커서 생성
        category = request.args.get('category')  # 쿼리 파라미터에서 category 가져오기
        if category:
            category = category.upper()  # 대문자로 변환

        search_text = request.args.get('searchText')  # 쿼리 파라미터에서 searchText 가져오기
        
        try:
            sql = "SELECT id, user_id, user_email, category, title, inserted_at, liked_count FROM posts WHERE 1=1"  # 기본 쿼리
            params = []

            if category:
                sql += " AND category = %s"  # 카테고리 필터 추가
                params.append(category)

            if search_text:
                sql += " AND title LIKE %s"  # 검색어 필터 추가
                params.append(f"%{search_text}%")  # LIKE 쿼리를 위한 패턴 추가

            cursor.execute(sql, params)  # 쿼리 실행
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]  # 컬럼명 가져오기
            return_result = []  
            for row in result:
                return_result.append(dict(zip(column_names, row)))  # 컬럼명과 값을 합쳐서 리스트로 반환
            
            return jsonify(result=return_result)
        except Exception as e:
            return jsonify(error=str(e))

@ROUTER.route('/posts/count')
class PostCountRoute(Resource):
    def get(self):
        """카테고리별 포스트 수 조회"""
        db = get_db_connection()  # 데이터베이스 연결 생성
        cursor = db.cursor()  # 커서 생성
        # 카테고리별 포스트 수 조회
        with db.cursor() as cursor:
            cursor.execute("SELECT category, COUNT(*) as post_count FROM posts GROUP BY category;")
            result = cursor.fetchall()
        
        # 결과를 요청한 형식으로 변환
        response = [{'category': category, 'count': post_count} for category, post_count in result]
        return jsonify(result=response)
    
    
@ROUTER.route('/posts/detail/<int:post_id>')
class PostDetailRoute(Resource):
    def get(self, post_id):
        """포스트 상세 조회"""
        try:
            sql = "SELECT * FROM posts WHERE id = %s"  # 포스트 ID로 조회
            cursor.execute(sql, (post_id,))  # 쿼리 실행
            result = cursor.fetchone()  # 단일 결과 가져오기
            
            if result:
                column_names = [desc[0] for desc in cursor.description]  # 컬럼명 가져오기
                return_result = dict(zip(column_names, result))  # 컬럼명과 값을 합쳐서 딕셔너리로 반환
                return jsonify(result=return_result)
            else:
                return jsonify(error="포스트를 찾을 수 없습니다."), 404  # 포스트가 없을 경우 오류 반환
        except Exception as e:
            return jsonify(error=str(e))