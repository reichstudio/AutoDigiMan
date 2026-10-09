"""Validate explicit image dependencies for canvas-ready asset pages."""
from pathlib import Path, PurePosixPath
import re
import base64
import binascii


def validate_asset_references(data, asset_root=None):
    errors = []
    assets = data.get('assets', [])
    by_id = {}
    for asset in assets:
        ident = asset.get('id', '')
        if not re.fullmatch(r'P[1-9][0-9]*', ident):
            errors.append(f'Invalid asset id: {ident!r}')
        if ident in by_id:
            errors.append(f'Duplicate asset id: {ident}')
        by_id[ident] = asset
    graph = {}
    for ident, asset in by_id.items():
        refs = asset.get('reference_ids')
        if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
            errors.append(f'{ident}: reference_ids must be an ordered string list (use [] for no references)')
            refs = []
        if len(refs) != len(set(refs)):
            errors.append(f'{ident}: duplicate reference_ids')
        graph[ident] = refs
        for ref in refs:
            if ref not in by_id:
                errors.append(f'{ident}: unknown reference {ref}')
        if asset.get('kind') == 'locked' and not asset.get('file'):
            errors.append(f'{ident}: locked asset requires file')
        filename = asset.get('file')
        if filename and str(filename).startswith('data:'):
            match = re.fullmatch(r'data:(image/(?:png|jpeg|webp|gif));base64,([A-Za-z0-9+/=]+)', str(filename))
            try:
                raw = base64.b64decode(match.group(2), validate=True) if match else b''
            except (ValueError, binascii.Error):
                raw = b''
            valid = bool(match and raw)
            if valid:
                mime = match.group(1)
                valid = ((mime == 'image/png' and raw.startswith(b'\x89PNG\r\n\x1a\n')) or
                         (mime == 'image/jpeg' and raw.startswith(b'\xff\xd8\xff')) or
                         (mime == 'image/gif' and raw[:6] in (b'GIF87a', b'GIF89a')) or
                         (mime == 'image/webp' and raw[:4] == b'RIFF' and raw[8:12] == b'WEBP'))
            if not valid:
                errors.append(f'{ident}: invalid embedded image data URI or image signature')
        elif filename:
            rel = PurePosixPath(str(filename))
            if rel.is_absolute() or '\\' in str(filename) or ':' in str(filename):
                errors.append(f'{ident}: file must be an HTML-relative path with forward slashes')
            elif asset_root is not None and not (Path(asset_root) / str(filename)).is_file():
                errors.append(f'{ident}: missing image file {filename}')
        if asset.get('kind') == 'generated':
            for field in ('prompt_en', 'prompt_zh'):
                mentions = set(re.findall(r'@(P[1-9][0-9]*)(?![A-Za-z0-9_])', asset.get(field, '')))
                if mentions != set(refs):
                    errors.append(f'{ident}: {field} @P mentions must match reference_ids')
    active, done = set(), set()

    def visit(ident):
        if ident in active:
            errors.append(f'Circular asset reference involving {ident}')
            return
        if ident in done:
            return
        active.add(ident)
        for ref in graph.get(ident, []):
            if ref in graph:
                visit(ref)
        active.remove(ident)
        done.add(ident)

    for ident in graph:
        visit(ident)
    return errors
