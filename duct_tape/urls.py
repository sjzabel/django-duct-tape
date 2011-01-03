def get_page(request):
    ''' Generic function to add the Page param '''
    page = 0
    page = page in request.GET and request.GET['page'] or 1 
    return { 'page': page }
