from typing import Dict
from django.core.cache import cache


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs) -> Dict[str, object]:
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context

class CacheMixin:

    def set_get_cache(self, request, query, cache_name: str, cache_time: int) -> Dict[str, object]:
        data = cache.get(cache_name)
        if not data:
            data = query
            cache.set(cache_name, data, cache_time)

        return data
