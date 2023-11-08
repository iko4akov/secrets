from rest_framework.pagination import PageNumberPagination


class SecretPaginator(PageNumberPagination):
    page_size = 5
