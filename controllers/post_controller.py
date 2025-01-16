from flask_restx import Namespace, Resource
from flask import jsonify
from blog_backend import db

import blog_backend.services.main_service as main_service

post = Namespace(name='posts', path='/posts', description='This api is posts')
cursor = db.cursor()

@post.route('/')
# @post.doc(params={'user_number': '파라미터로 입력된 숫자'})
@post.header('content-type', 'application/json')
class PostRoute(Resource):
    def get(self) -> str:
        """포스트 조회"""
        try:
            sql = "select * from posts"
            cursor.execute(sql)
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]  # 컬럼명 가져오기
            return_result = []  
            for row in result:
                return_result.append(dict(zip(column_names, row)))  # 컬럼명과 값을 합쳐서 리스트로 반환
            return jsonify(result=return_result)
        except Exception as e:
            return jsonify(error=str(e))

@post.route('/count')
class PostCountRoute(Resource):
    def get(self):
        """카테고리별 포스트 수 조회"""
        # 카테고리별 포스트 수 조회
        with db.cursor() as cursor:
            cursor.execute("SELECT category, COUNT(*) as post_count FROM posts GROUP BY category;")
            result = cursor.fetchall()
        
        # 결과를 요청한 형식으로 변환
        response = [{'category': category, 'count': post_count} for category, post_count in result]
        return jsonify(result=response)