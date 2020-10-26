from django.template import loader
from haystack import indexes

from .models import GFile


class GFileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField()

    def get_model(self):
        return GFile

    def prepare_title(self, obj):
        return obj.title

    def prepare(self, obj):
        data = super().prepare(obj)

        # This could also be a regular Python open() call, a StringIO instance
        # or the result of opening a URL. Note that due to a library limitation
        # file_obj must have a .name attribute even if you need to set one
        # manually before calling extract_file_contents:
        file_obj = obj.file.open()

        extracted_data = self.get_backend().extract_file_contents(file_obj)
        # Now we'll finally perform the template processing to render the
        # text field with *all* of our metadata visible for templating:
        t = loader.select_template(("search/indexes/drive/gfile_text.txt",))
        data["text"] = t.render({"object": obj, "extracted": extracted_data})

        return data
