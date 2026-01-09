from django.utils.dateparse import parse_date

def filtrar_facturas_por_fecha(request, queryset):
    fecha = request.query_params.get("fecha")
    fecha_inicio = request.query_params.get("fecha_inicio")
    fecha_fin = request.query_params.get("fecha_fin")

    if fecha:
        queryset = queryset.filter(fecha=parse_date(fecha))

    if fecha_inicio and fecha_fin:
        queryset = queryset.filter(
            fecha__range=[
                parse_date(fecha_inicio),
                parse_date(fecha_fin)
            ]
        )

    return queryset