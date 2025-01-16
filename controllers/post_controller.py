from flask_restx import Namespace, Resource
from flask import jsonify, request
from blog_backend import db

import blog_backend.services.main_service as main_service

ROUTER = Namespace(name='Main Api들', path='/', description='This api is posts')
cursor = db.cursor()

@ROUTER.route('/posts')
@ROUTER.doc(params={'category': '파라미터로 입력된 카테고리'})
@ROUTER.doc(params={'searchText': '파라미터로 입력된 검색어'})
@ROUTER.header('content-type', 'application/json')
class PostRoute(Resource):
    def get(self) -> str:
        """포스트 조회"""
        category = request.args.get('category')  # 쿼리 파라미터에서 category 가져오기
        if category:
            category = category.upper()  # 대문자로 변환

        search_text = request.args.get('searchText')  # 쿼리 파라미터에서 searchText 가져오기
        
        try:
            sql = "SELECT * FROM posts WHERE 1=1"  # 기본 쿼리
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
        # 카테고리별 포스트 수 조회
        with db.cursor() as cursor:
            cursor.execute("SELECT category, COUNT(*) as post_count FROM posts GROUP BY category;")
            result = cursor.fetchall()
        
        # 결과를 요청한 형식으로 변환
        response = [{'category': category, 'count': post_count} for category, post_count in result]
        return jsonify(result=response)