"""Dependency-free ASCII DXF reader for plan linework.

Supports LINE, LWPOLYLINE and legacy POLYLINE/VERTEX/SEQEND entities,
which are used by the supplied Japanese architectural drawings.  The reader
keeps the source layer so callers can filter walls, doors and windows without
requiring ezdxf inside Blender.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DXFSegment:
    start: tuple[float, float]
    end: tuple[float, float]
    layer: str


def _pairs(text: str):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if len(lines) % 2:
        lines = lines[:-1]
    for index in range(0, len(lines), 2):
        try:
            code = int(lines[index].strip())
        except ValueError:
            continue
        yield code, lines[index + 1].strip()


def _entities(pairs):
    current = []
    in_entities = False
    section_pending = False
    for code, value in pairs:
        if code == 0 and value == "SECTION":
            section_pending = True
            continue
        if section_pending and code == 2:
            in_entities = value == "ENTITIES"
            section_pending = False
            continue
        if code == 0 and value == "ENDSEC":
            if current and in_entities:
                yield current
            current = []
            in_entities = False
            continue
        if not in_entities:
            continue
        if code == 0:
            if current:
                yield current
            current = [(code, value)]
        elif current:
            current.append((code, value))
    if current and in_entities:
        yield current


def _first(entity, code, default=None):
    for item_code, value in entity:
        if item_code == code:
            return value
    return default


def _float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _line(entity):
    x1, y1 = _float(_first(entity, 10)), _float(_first(entity, 20))
    x2, y2 = _float(_first(entity, 11)), _float(_first(entity, 21))
    if None in (x1, y1, x2, y2):
        return None
    return DXFSegment((x1, y1), (x2, y2), _first(entity, 8, "0"))


def _segments(points, layer, closed=False):
    result = [
        DXFSegment(start, end, layer)
        for start, end in zip(points, points[1:])
        if start != end
    ]
    if closed and len(points) > 2 and points[-1] != points[0]:
        result.append(DXFSegment(points[-1], points[0], layer))
    return result


def _lwpolyline(entity):
    layer = _first(entity, 8, "0")
    flags = int(_first(entity, 70, "0") or 0)
    points = []
    pending_x = None
    for code, value in entity:
        if code == 10:
            pending_x = _float(value)
        elif code == 20 and pending_x is not None:
            y = _float(value)
            if y is not None:
                points.append((pending_x, y))
            pending_x = None
    return _segments(points, layer, bool(flags & 1))


def _polyline(entity):
    """Read an R12-style POLYLINE followed by VERTEX records.

    _entities keeps VERTEX and SEQEND as separate records.  This helper
    consumes the complete three-record sequence and is called by
    _legacy_polylines below.
    """
    flags = int(_first(entity, 70, "0") or 0)
    return _first(entity, 8, "0"), bool(flags & 1)


def _legacy_polylines(entities):
    result = []
    index = 0
    while index < len(entities):
        entity = entities[index]
        if entity[0][1] != "POLYLINE":
            index += 1
            continue

        layer, closed = _polyline(entity)
        points = []
        index += 1
        while index < len(entities):
            child = entities[index]
            entity_type = child[0][1]
            if entity_type == "VERTEX":
                x, y = _float(_first(child, 10)), _float(_first(child, 20))
                if x is not None and y is not None:
                    points.append((x, y))
                index += 1
                continue
            if entity_type == "SEQEND":
                index += 1
            break
        result.extend(_segments(points, layer, closed))
    return result


def read_segments(path: str) -> list[DXFSegment]:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(path)
    raw = file_path.read_bytes()
    if raw.startswith(b"AutoCAD Binary DXF"):
        raise ValueError("Binary DXF is not supported; save as ASCII DXF")

    text = None
    for encoding in ("utf-8-sig", "cp932", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise ValueError("Unable to decode DXF")

    entities = list(_entities(_pairs(text)))
    result = []
    for entity in entities:
        entity_type = entity[0][1]
        if entity_type == "LINE":
            segment = _line(entity)
            if segment:
                result.append(segment)
        elif entity_type == "LWPOLYLINE":
            result.extend(_lwpolyline(entity))
    result.extend(_legacy_polylines(entities))
    return result


def layer_matches(layer: str, filter_text: str) -> bool:
    tokens = [token.strip().lower() for token in filter_text.split(",") if token.strip()]
    return not tokens or any(token in layer.lower() for token in tokens)
