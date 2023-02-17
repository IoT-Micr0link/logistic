from django_tables2 import tables


class TableBase(tables.Table):
    class Meta:
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        attrs = {
            "class": "table",
            "thead": {
                "class": "thead-dark"
            }
        }