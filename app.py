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
