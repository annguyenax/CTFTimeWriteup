# Bliss I solver

Run from any directory:

```powershell
python "D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\solve\solve.py"
```

The solver reads the archived Svelte route node and CSS in `evidence/`. It maps
the highlighted `square-N` selectors back to the 64 characters embedded in the
route node, preserving the clue order shown by `runes.png`.
