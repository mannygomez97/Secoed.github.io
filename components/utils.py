from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
from django.http import HttpResponse
from django.template.loader import get_template
#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.
from xhtml2pdf import pisa
def render_to_pdf_2(request, template_src, context_dict={}):
    pass



def render_to_pdf(request, template_src, context_dict={}):
    project_url = request.get_host() + '/templates/components/pdf'
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    #This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="test.pdf"'
        return response
    return HttpResponse("Error ?")