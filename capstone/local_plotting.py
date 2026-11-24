"""Use only repository-local configuration and bundled fonts."""
from pathlib import Path
import json
import os
import re


def configure():
    root = Path(__file__).resolve().parents[1]
    work = root / '.git/capstone-build'
    work.mkdir(exist_ok=True)
    for name in ['MPLCONFIGDIR', 'XDG_CACHE_HOME', 'TMPDIR', 'IPYTHONDIR', 'JUPYTER_CONFIG_DIR', 'JUPYTER_DATA_DIR', 'JUPYTER_RUNTIME_DIR']:
        path = work / name.lower()
        path.mkdir(exist_ok=True)
        os.environ[name] = str(path)
    os.environ['MPLBACKEND'] = 'Agg'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    mpl = next((root / '.venv/lib').glob('python*/site-packages/matplotlib'))
    version = re.search(r"__version__ = ['\"]([^'\"]+)", (mpl / 'font_manager.py').read_text())[1]
    entries = []
    for filename, style, weight in [('DejaVuSans.ttf', 'normal', 400), ('DejaVuSans-Bold.ttf', 'normal', 700), ('DejaVuSans-Oblique.ttf', 'oblique', 400)]:
        font = mpl / 'mpl-data/fonts/ttf' / filename
        assert font.resolve().is_relative_to(root)
        entries.append(dict(__class__='FontEntry', fname=str(font), index=0, name='DejaVu Sans', style=style, variant='normal', weight=weight, stretch='normal', size='scalable'))
    cache = dict(__class__='FontManager', _version=version, _FontManager__default_weight='normal', default_size=None, defaultFamily={'ttf': 'DejaVu Sans', 'afm': 'Helvetica'}, afmlist=[], ttflist=entries)
    (Path(os.environ['MPLCONFIGDIR']) / f'fontlist-v{version}.json').write_text(json.dumps(cache))
    rc = work / 'matplotlibrc'
    rc.write_text('font.family: DejaVu Sans\nbackend: Agg\n')
    os.environ['MATPLOTLIBRC'] = str(rc)
    return root
