"""
Peritos v3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError
from lib.safe_string import safe_string

from ...core.peritos.models import Perito
from ..distritos.crud import get_distrito, get_distrito_with_clave
from ..peritos_tipos.crud import get_perito_tipo


def get_peritos(
    db: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
    nombre: str = None,
    perito_tipo_id: int = None,
) -> Any:
    """Consultar los peritos activos"""
    consulta = db.query(Perito)
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None and distrito_clave != "":
        distrito = get_distrito_with_clave(db, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    if nombre is not None:
        nombre = safe_string(nombre)
        if nombre != "":
            consulta = consulta.filter(Perito.nombre.contains(nombre))
    if perito_tipo_id is not None:
        perito_tipo = get_perito_tipo(db, perito_tipo_id)
        consulta = consulta.filter_by(perito_tipo_id=perito_tipo.id)
    return consulta.filter_by(estatus="A").order_by(Perito.nombre)


def get_perito(db: Session, perito_id: int) -> Perito:
    """Consultar un perito por su id"""
    perito = db.query(Perito).get(perito_id)
    if perito is None:
        raise MyNotExistsError("No existe ese perito")
    if perito.estatus != "A":
        raise MyIsDeletedError("No es activo ese perito, está eliminado")
    return perito
