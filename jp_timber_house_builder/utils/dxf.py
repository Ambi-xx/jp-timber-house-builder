"""Small dependency-free ASCII DXF reader for plan linework.

Supported entities: LINE and LWPOLYLINE. This intentionally avoids an
external ezdxf dependency so the add-on can be installed as a normal Blender
ZIP. Binary DXF files are rejected with a clear error.
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


def _line(entity):
    try:
        return DXFSegment(
            (float(_first(entity, 10)), float(_first(entity, 20))),
            (float(_first(entity, 11)), float(_first(entity, 21))),
            _first(entity, 8, "0"),
        )
    except (TypeError, ValueError):
        return None


def _lwpolyline(entity):
    layer = _first(entity, 8, "0")
    flags = int(_first(entity, 70, "0") or 0)
    points = []
    pending_x = None
    for code, value in entity:
        if code == 10:
            try:
                pending_x = float(value)
            except ValueError:
                pending_x = None
        elif code == 20 and pending_x is not None:
            try:
                points.append((pending_x, float(value)))
            except ValueError:
                pass
            pending_x = None
    segments = [DXFSegment(a, b, layer) for a, b in zip(points, points[1:])]
    if flags & 1 and len(points) > 2:
        segments.append(DXFSegment(points[-1], points[0], layer))
    return segments


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

    result = []
    for entity in _entities(_pairs(text)):
        entity_type = entity[0][1]
        if entity_type == "LINE":
            segment = _line(entity)
            if segment:
                result.append(segment)
        elif entity_type == "LWPOLYLINE":
            result.extend(_lwpolyline(entity))
    return result


def layer_matches(layer: str, filter_text: str) -> bool:
    tokens = [token.strip().lower() for token in filter_text.split(",") if token.strip()]
    return not tokens or any(token in layer.lower() for token in tokens)
