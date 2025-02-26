from scrapy.exporters import CsvItemExporter

# Разделитель ";" для коррекктной работы csv
class CsvCustomSeperator(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-8-sig'
        kwargs['delimiter'] = ';'
        super(CsvCustomSeperator, self).__init__(*args, **kwargs)