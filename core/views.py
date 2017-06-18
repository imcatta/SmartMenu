from django.contrib.admin.views.decorators import staff_member_required
from django import http
import xhtml2pdf.pisa as pisa
from django.shortcuts import render_to_response
from django.template.loader import get_template
from io import BytesIO
import cgi
from django.shortcuts import get_object_or_404
from core.models import Menu


@staff_member_required
def get_menu_pdf(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    return render_to_pdf('core/pdf/menu.html', {'menu': menu})


def render_to_pdf(template_src, context):
    template = get_template(template_src)
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(str(html), dest=result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), content_type='application/pdf')
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))