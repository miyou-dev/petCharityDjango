from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    # 默认每页显示10个
    page_size = 5
    page_size_query_param = "size"
    page_size_query_description = '每页显示的个数'
    # 获取页码数的
    page_query_param = "page"
    page_query_description = '页码数'
    # 最大页数
    max_page_size = 50
