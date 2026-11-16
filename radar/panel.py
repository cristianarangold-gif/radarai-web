"""«Mi panel»: precios en euros de la última toma para autocompletar las suscripciones del visitante."""
from __future__ import annotations

from typing import Dict

from radar.price_history import Snapshot, parse_price

CICLOS = {'/mes': 'mensual', '/año': 'anual', '': 'mensual'}


def panel_prices(snapshot: Snapshot, names: Dict[str, str]) -> dict:
    """{fecha, herramientas: {id: {nombre, planes: {plan: {texto, euros, ciclo, desde}}}}}, solo planes en euros."""
    tools = {}
    for tool, data in sorted(snapshot.tools.items()):
        planes = {}
        for plan, value in (data.get('planes') or {}).items():
            price = parse_price(value)
            if not price or price.currency != '€' or price.period not in CICLOS:
                continue
            planes[plan] = {'texto': price.text, 'euros': float(price.amount),
                            'ciclo': CICLOS[price.period], 'desde': price.desde}
        if planes:
            tools[tool] = {'nombre': names.get(tool, tool), 'planes': planes}
    return {'fecha': snapshot.date, 'herramientas': tools}
