# Práctica de n8n
En este proyecto de práctica se realizó un sistema de prueba básico de recomendación de productos, con la finalidad de demostrar el aprendizaje en el uso de n8n para la orquestación de tareas.
Primero se realizó la extracción de datos de los productos del sumermercado D1 utilizando python, se logró obtener la información más relevante mostrada en el frontend de la plataforma: nombre del producto, precio, peso, imagen, descripción y link de referencia; una vez obtenidos los datos se exportaron a un csv y posteriormente se cargaron en una hoja de Google Sheets: https://docs.google.com/spreadsheets/d/1kJcTPaGKKvz60V3syWTJCNn6qoDoSx5tAKplhP2XVKc/edit?usp=sharing.

Partiendo de los datos obtenidos se comenzó a realizar el flujo de trabajo, primero importando la hoja de cálculo de Google Sheets y realizando el filtrado de columnas, posteriormente se tomó una muestra aleatoria de cinco productos y se estandarizó un mensaje de promoción para finalmente enviarse por correo electrónico.


