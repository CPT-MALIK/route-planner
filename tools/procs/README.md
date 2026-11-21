# Approach drawing pipeline (session 7)

Source: eAIP AD 2 "(aeronautical data tabulation)" PDFs (one page each, text is an image; read visually).

- `stk.py <ICAO>`: renders the tabulation PDFs of an airport (from `/tmp/t2/src` or `/tmp/t3/src`, the user's zips unpacked) into stacked crops `/tmp/w/<ICAO>/S*.png` for reading.
- `chv.py <ICAO> "<chart title>" ...`: crops the app's own approach charts (`charts/<ICAO>/...webp`) for checking arcs / missed approaches.
- `lib.py`: helpers. `check()` verifies typed coordinates against tabulated course/distance and radial/DME (flags >1.5° or >0.3 NM). `rnp()` builds RNAV procedures from transitions; `conv()` builds conventional ones (DME arc / straight to IF, FAF, MAP, simplified missed approach + hold). `emit()` writes `PROCS.<ICAO>=...;`; `ins()` inserts or replaces it in index.html (before `const procP=n=>`).
- `b1.py` .. `b7.py`, `oerr.py`, `oesn.py`, ... : the data actually used, per airport (paths point to /tmp/gw; copy the folder there to rerun).
- `shot2.py ICAO:index ...`: Playwright screenshots of drawn procedures (uses `window.__procSet(icao,i,true)`).
