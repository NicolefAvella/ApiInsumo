from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
      
        name = args[0].request.data.get("name", "")
        machine = args[0].request.data.get("machine", "")
        if not name and not machine:
            return Response(
                data={
                    "message": "Es requerido nombre del insumo y la maquina a la que pertenece"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated