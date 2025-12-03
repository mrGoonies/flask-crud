from flask import Flask, request
from typing import List

app = Flask(__name__)


stores: List[dict] = [
    {
        "name": "Store 1",
        "items": [
            {
                "name": "Item A",
                "price": 10.99,
                "quantity": 5,
            },
            {
                "name": "Item B",
                "price": 5.49,
                "quantity": 10,
            },
        ],
    },
    {
        "name": "Store 2",
        "items": [
            {
                "name": "Item C",
                "price": 7.99,
                "quantity": 3,
            }
        ],
    },
]


@app.get("/stores")
def get_stores() -> dict:
    """Devuelve el nombre y items para cada tienda almacenada.

    Returns:
        dict: Un diccionario con la lista de tiendas y sus items.
    """
    return {"stores": stores}


@app.post("/store")
def create_store() -> str:
    """Creamos una nueva tienda y almacenamos en la list.

    Returns:
        str: Mensaje de confirmación.
    """
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}

    for store in stores:
        if store["name"] == new_store["name"]:
            return "La tienda ya existe", 404

    # Si no existe, agregar la nueva tienda y retornar 201
    stores.append(new_store)
    return "Se ha creado la nueva tienda", 201


@app.post("/store/<string:store_name>/item")
def create_item_for_store(store_name: str) -> str:
    """Agregamos items para una tienda en especifico.

    Args:
        store_name (str): Nombre de la tienda a trabajar.

    Returns:
        str: Mensaje descriptivo respecto a la accion que se realizo.
    """
    request_data = request.get_json()
    post_data: dict = {
        "name": request_data["name"],
        "price": request_data["price"],
        "quantity": request_data["quantity"],
    }

    for store in stores:
        if store["name"] == store_name:
            store["items"].append(post_data)
            return "Item agregado a tienda especificada con éxito.", 201
    return "La tienda no existe.", 404


@app.get("/store/<string:store_name>")
def get_specific_store_data(store_name: str):
    """Obtenemos todos los items que se encuentran almacenados en una tienda especifica junto al nombre de la tienda

    Args:
        store_name (str): Nombre de la tienda a listar items almacenados.

    Returns:
        Si la tienda existe, devuelve el diccionario con todos los items almacenados para la tienda, en caso contrario, devuelve un mensaje indicando que la tienda no existe.
    """
    for store in stores:
        if store["name"] == store_name:
            return store, 201
    return "La tienda ingresada no existe", 404


@app.get("/store/<string:name>/items")
def get_items_for_store(name):
    """Obtener items almacenados dentro de una tienda creada

    Args:
        name (str): Nombre de la tienda a mostrar items almacenados.

    """
    for store in stores:
        if store["name"] == name:
            return store["items"], 201
    return "La tienda ingresada no existe", 404
