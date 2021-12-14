~~~~# Nubi Encuestas

Dado el siguiente listado de features solicitadas por el Product Owner (PO):

- Quiero tener una API que me permita crear encuestas.
- Quiero poder responder cada encuesta muchas veces.
- Quiero poder acceder a un listado de todas las encuestas y sus respuestas.

el equipo de desarrollo realizó un MVP de la API en Python utilizando Flask. Ahora necesitamos hacer un refactor para poder encarar una nueva etapa de desarrollo y trabajar sobre bases más sólidas.

Por esto, te pedimos que revises el código y nos entregues:

- Una lista priorizada con los puntos débiles que hayas encontrado, justificando por qué son un problema y proponiendo una mejora para cada uno
- La implementación de los puntos más críticos que hayas encontrado (al menos 3)

No hace falta analizar la parte de infraestructura, poné el foco en el código Python.

Para ayudarte, el equipo de desarrollo preparó algunos ejemplos de uso de la API:

`curl http://localhost:5000`

`curl http://localhost:5000/addPoll --request GET --header "Content-Type: application/json" --data '{"question": "¿Te gusta Python?"}'`

`curl http://localhost:5000/addAnswer --request GET --header "Content-Type: application/json" --data '{"poll_id": "5fc9129482d4589e8d7d687e", "answer": "Me encanta Python"}'`

`curl http://localhost:5000/getPolls`

Las propuestas que hagas pueden ser de cualquier tipo, siempre que sean coherentes entre sí.

Podés preguntar cualquier duda que tengas respecto a los requerimientos del PO.

La solución del ejercicio deberás subirla a un repositorio privado, darnos acceso compartirnos el link.

El commit original tendrá que ser con los archivos tal cual te los damos.

Cada propuesta que elijas implementar deberá ser desarrollada en un commit independiente.

La documentación de la solución (problemas encontrados y justificaciones) también deberá estar en el mismo repo. Podés usar el formato que prefieras, mientras más detallado mejor.

Las soluciones para mejorar puntos débiles que se implementaron fueron las siguientes:
Validación de usuarios para evitar que cualquier persona pueda acceder a crear encuestas y responderlas, así como leerlas.
Ademas se limita la cantidad de requests por unidad de tiempo para minimizar la posibilidad de ataques de denegación de servicio.
Tambien se implementó el chequeo del formato de la información enviada en los requests.
Por otro lado, otras cuestiones a mejorar podrian ser cambiar el método de requests, al agregar preguntas y sus respectivas
respuestas, de GET a POST para ocultar los datos al usuario web. Se podría agregar un método para eliminar preguntas y respuestas.
En el caso de getPolls, por ejemplo, se podría implementar que la busqueda de las respuestas la haga el motor de base de datos
y evitar tener que obtener la totalidad de las respuestas. En el caso de tener muchas respuestas, esto puede afectar la 
performance.
Con respecto a lo implementado en los metodos registration() y login(), las contraseñas deberian almacenarse encriptadas
en la base de datos y enviar los requests a traves de un canal seguro.