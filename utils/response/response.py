from rest_framework import response


class Response(response.Response):

    @staticmethod
    def code_detail(code: int, detail: str, status=None, template_name=None, headers=None, exception=False,
                    content_type=None):
        return Response({'code': code, 'detail': detail}, status, template_name, headers, exception, content_type)

    @staticmethod
    def code_data(code: int, detail: str, data, status=None, template_name=None, headers=None, exception=False,
                  content_type=None):
        return Response({'code': code, 'detail': detail, 'data': data}, status, template_name, headers, exception,
                        content_type)

    @staticmethod
    def whether_detail(code: int, whether: int, detail: str, status=None, template_name=None, headers=None,
                       exception=False, content_type=None):
        return Response({'code': code, 'whether': whether, 'detail': detail}, status, template_name, headers, exception,
                        content_type)
