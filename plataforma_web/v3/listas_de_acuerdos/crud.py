"""
Listas de Acuerdos v3, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.autoridades.models import Autoridad
from ...core.listas_de_acuerdos.models import ListaDeAcuerdo
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_listas_de_acuerdos(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    anio: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar las listas de acuerdos activas"""
    consulta = db.query(ListaDeAcuerdo)
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_with_clave(db, autoridad_clave)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(db, distrito_clave)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    if anio is not None:
        desde = date(year=anio, month=1, day=1)
        hasta = date(year=anio, month=12, day=31)
        consulta = consulta.filter(ListaDeAcuerdo.fecha >= desde).filter(ListaDeAcuerdo.fecha <= hasta)
    elif fecha is not None:
        consulta = consulta.filter(ListaDeAcuerdo.fecha == fecha)
    else:
        if fecha_desde is not None:
            consulta = consulta.filter(ListaDeAcuerdo.fecha >= fecha_desde)
        if fecha_hasta is not None:
            consulta = consulta.filter(ListaDeAcuerdo.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(ListaDeAcuerdo.id.desc())


def get_lista_de_acuerdo(db: Session, lista_de_acuerdo_id: int) -> ListaDeAcuerdo:
    """Consultar una lista de acuerdo por su id"""
    lista_de_acuerdo = db.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise MyNotExistsError("No existe ese lista de acuerdo")
    if lista_de_acuerdo.estatus != "A":
        raise MyIsDeletedError("No es activo ese lista de acuerdo, está eliminado")
    return lista_de_acuerdo
