import contextlib

from rest_framework.pagination import PageNumberPagination


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


class CustomPostPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'current'
    page_size_query_param = 'pageSize'
    max_page_size = 1000
    pagination_query_param = 'pagination'

    def get_page_number(self, request, paginator):
        page_number = request.data.get(self.pagination_query_param, {}).get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        return page_number

    def get_page_size(self, request):
        if self.page_size_query_param:
            with contextlib.suppress(KeyError, ValueError):
                return _positive_int(
                    request.data[self.pagination_query_param][self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )

        return self.page_size
