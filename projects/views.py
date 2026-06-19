from django.shortcuts import render, get_object_or_404
from projects.models import Proyecto
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # ← solo si NO usas csrf en fetch
from django.views.decorators.http import require_POST
from .models import IdeaPrivada
import json
from rest_framework import viewsets
from .models import Proyecto
from .api import ProyectoSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from ollama import Client

@ensure_csrf_cookie
def dashboard_proyectos(request):
    proyectos = Proyecto.objects.all().order_by('titulo') 
    return render(request, 'projects/dashboard_proyectos.html')
    
class ProyectoViewSet(viewsets.ModelViewSet):  
    queryset = Proyecto.objects.all().order_by('titulo')
    serializer_class = ProyectoSerializer

def idea_mejorar_view(request, pk):
    idea = get_object_or_404(Proyecto, pk=pk)
    
    context = {
        'idea': idea,
        'titulo_original': idea.titulo,
        'descripcion_original': idea.categoria,  
    }
    return render(request, 'projects/idea_mejorar.html', context)
    

@require_POST
@csrf_exempt
def crear_idea(request):
    try:
        print("BODY:", request.body)  
        data = json.loads(request.body)
        print("DATA PARSED:", data)    

        titulo = data.get('titulo', '').strip()
        descripcion = data.get('descripcion', '').strip()

        if not titulo or not descripcion:
            return JsonResponse({"error": "Faltan título o descripción"}, status=400)

        idea = IdeaPrivada.objects.create(
            titulo=titulo,
            descripcion=descripcion,
        )
        return JsonResponse({"status": "ok"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



def mejorar_descripcion(request):
    if request.method != "POST":
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        texto = data.get('texto', '').strip()

        if not texto:
            return JsonResponse({'ok': False, 'error': 'Texto vacío'}, status=400)

        client = Client()

        response = client.chat(
            model="llama2",  
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto en startups y redactas ideas de forma profesional y clara."
                },
                {
                    "role": "user",
                    "content": f"Mejora y amplía esta idea:\n\n{texto}"
                }
            ]
        )

        # ✅ AQUÍ ESTÁ LA CLAVE
        descripcion_mejorada = response["message"]["content"]

        return JsonResponse({
            'ok': True,
            'descripcion_mejorada': descripcion_mejorada
        })

    except Exception as e:
        print("ERROR OLLAMA:", str(e))  
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)
    


