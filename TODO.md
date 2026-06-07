# TODO

## Template duplication consolidation
- [x] Confirm Django template search path (`Toolson/Toolson/settings.py` uses `BASE_DIR / 'template'` → `c:/2LSN/Toolson/template`).
- [ ] Move every file from `c:/2LSN/template/` into a backup folder `c:/2LSN/template_unused_backup/`.
- [ ] Remove remaining files from `c:/2LSN/template/` (keep folder if empty).
- [ ] Run `python manage.py check` and a quick template render smoke test.

