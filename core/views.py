from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SecurityIncident  # Importem el model per usar l'ORM
from django.shortcuts import render, get_object_or_404 # Importem l'ajudant 404

@login_required
def perfil_usuari(request):
    return render(request, 'perfil.html')

def cerca_incidents(request):
    query = request.GET.get('q', '')
    incidents = []

    if query:
        # HARDENING: L'ORM de Django parametritza automàticament l'entrada.
        # Això evita que payloads com ' OR '1'='1 executin codi maliciós.
        incidents = SecurityIncident.objects.filter(title__icontains=query)

    return render(request, 'core/cerca.html', {'incidents': incidents, 'query': query})

@login_required
def actualitzar_correu(request):
    email = request.GET.get('email', '')
    if email:
        # HARDENING: No usem SQL manual per actualitzar l'usuari.
        # L'ús de l'objecte request.user amb .save() és segur i impedeix
        # que un atacant modifiqui camps com 'is_superuser'.
        request.user.email = email
        request.user.save()

    return render(request, 'core/actualitzar_correu.html', {'email': email})

@login_required
def detall_incident(request, id):
    # HARDENING: Implementem control d'accés a nivell de fila.
    # Busquem l'incident per ID PERÒ restringit al creador (request.user).
    # Si la ID existeix però pertany a un altre usuari, Django llançarà un 404 automàticament.
    incident = get_object_or_404(SecurityIncident, id=id, user=request.user)

    return render(request, 'core/detall_incident.html', {'incident': incident})
