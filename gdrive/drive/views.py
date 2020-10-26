from haystack.views import SearchView


class PeriodicalSearchView(SearchView):
    def get_results(self):
        """
        Fetches the results via the form.
        Returns an empty list if there's no query to search with.
        """
        if not (self.form.is_valid() and self.form.cleaned_data["q"]):
            return self.form.no_query_found()

        query = self.form.cleaned_data["q"]

        words = iter(set(query.split()))
        word = next(words)
        sqs = self.form.searchqueryset.filter(
            text=word
        )  # actually I have one more field here...
        for word in words:
            sqs = sqs.filter_or(title=word).filter_or(text=word)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def __call__(self, request, template_name=None):
        """
        Generates the actual response to the search.
        Relies on internal, overridable methods to construct the response.
        """
        if template_name:
            self.template = template_name

        return super(PeriodicalSearchView, self).__call__(request)
