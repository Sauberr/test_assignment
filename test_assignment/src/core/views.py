from django.views.generic import TemplateView, DetailView, ListView
from django_elasticsearch_dsl.search import Search
from elasticsearch_dsl.query import Q
from .models import Books

from account.services.mixins import TitleMixin
from django.http import JsonResponse
from .documents import BookDocument

class IndexView(TitleMixin, TemplateView):
    template_name: str = "partials/index.html"
    title: str = "Home"

    # @staticmethod
    # def get_search_results(query, correction: bool = False, size: int = 5):
    #     query = query.lower()
    #     search_query = Q(
    #         "bool",
    #         should=[
    #             Q("multi_match", query=query, fields=['title^7', 'author^2', 'description'],
    #               fuzziness='AUTO', prefix_length=2, operator='and'),
    #             Q("wildcard", title={"value": f"*{query}*", "boost": 7}),
    #             Q("wildcard", author={"value": f"*{query}*", "boost": 2}),
    #             Q("wildcard", description={"value": f"*{query}*"}),
    #         ],
    #         minimum_should_match=1
    #     )
    #     search = BookDocument.search().query(search_query)[0:size if correction else None]
    #     results = [hit.to_dict() for hit in search]
    #     return results
    #
    # @staticmethod
    # def get_correction_query(query):
    #     suggest = Search(index="books")
    #     for field in ['title', 'author', 'description']:
    #         suggest = suggest.suggest(f'{field}_suggestion', query, term={'field': field})
    #     response = suggest.execute()
    #
    #     best_correction = query
    #     for suggestion in response.suggest:
    #         if response.suggest[suggestion][0].options:
    #             best_correction = response.suggest[suggestion][0].options[0].text
    #             break
    #     return best_correction if best_correction != query else None
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     query = self.request.GET.get('q')
    #     if query:
    #         context['original_query'] = query
    #         books = self.get_search_results(query)
    #         correction = self.get_correction_query(query)
    #         if correction and correction.lower() != query.lower():
    #             context['correction'] = correction
    #             corrected_books = self.get_search_results(correction)
    #             if corrected_books:
    #                 context['books'] = corrected_books
    #             else:
    #                 context['books'] = books
    #         else:
    #             context['books'] = books
    #             context['correction'] = None
    #     else:
    #         search = Search(index="books")
    #         response = search.scan()
    #         context['books'] = [hit.to_dict() for hit in response]
    #         context['correction'] = None
    #     return context
    #
    # def get(self, request, *args, **kwargs):
    #     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #         query = request.GET.get('q', '')
    #         suggestions = self.get_search_results(query, correction=True) if query else []
    #         if not suggestions:
    #             correction = self.get_correction_query(query)
    #             if correction and correction.lower() != query.lower():
    #                 suggestions = self.get_search_results(correction, correction=True)
    #                 suggestions.append({'correction': correction, 'original_query': query})
    #         return JsonResponse(suggestions, safe=False)
    #     return super().get(request, *args, **kwargs)


class BookList(TitleMixin, ListView):
    template_name: str = "partials/books_list.html"
    title: str = "Books"
    model = Books
    context_object_name: str = 'books'
    ordering = ['title']

