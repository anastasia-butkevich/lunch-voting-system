class AppVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.app_build = request.headers.get('X-App-Build', None)
        return self.get_response(request)
    