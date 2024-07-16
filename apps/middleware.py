# To Get The Last page user has visited

class LastPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get response for the current request
        response = self.get_response(request)
        
        # Store the current path before sending the response
        if request.method == 'GET' and request.path not in ['/favicon.ico', '/robots.txt']:  # Exclude some paths
            request.session['last_page'] = request.path

        return response