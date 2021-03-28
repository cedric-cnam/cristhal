from django.shortcuts import render
import logging


def index(request):
    context = {"titre": "Accueil", 
               "css_sous_menu_accueil": "current_page_item"}
    
    logger = logging.getLogger("malachia")
    
    logger.info('Message de log')
    return render(request, 'accueil/index.html', context)
