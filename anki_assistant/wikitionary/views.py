from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dictionary


class WordView(APIView):
    def get(self, request, identifier):
        dict = Dictionary(settings.INPUT_FILEPATH)
        word = dict.search_word(identifier)

        mode = request.query_params.get('mode')
        if mode == 'annotated':
            return Response(word.as_annotated_json())
        return Response(word.as_json())
