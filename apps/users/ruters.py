from django.urls import path

class MyRouter:
    def __init__(self):
        self.routes = []

    def add_router(self, route, view):
        self.routes.append((route, view))

    def get_urlpatterns(self):
        urlpatterns = []
        for route, view in self.routes:
            urlpatterns.append(path("reset-new-password/<int:token>", view.as_view(), name=None))
        return urlpatterns