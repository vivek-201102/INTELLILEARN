from urllib.parse import urlencode

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


def get_search_term(request, param='q'):
    return request.GET.get(param, '').strip()


def pagination_query_string(request, exclude=None):
    """Build query string preserving filters (excludes page by default)."""
    if exclude is None:
        exclude = {'page'}
    pairs = []
    for key in request.GET:
        if key in exclude:
            continue
        value = request.GET.get(key, '').strip()
        if value:
            pairs.append((key, value))
    return urlencode(pairs)


def paginate(request, queryset, per_page=10, page_param='page'):
    """Return a Page object for the current request."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get(page_param, 1)

    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def list_page_context(request, page_obj, search_placeholder='Search…'):
    """Standard context for searchable, paginated list pages."""
    q = get_search_term(request)
    return {
        'page_obj': page_obj,
        'q': q,
        'query_string': pagination_query_string(request),
        'search_placeholder': search_placeholder,
        'has_filters': bool(q),
    }
