"""One-off API exploration — run manually."""
import inspect

import sportsdataverse.pwhl as pwhl
import sportsdataverse.wnba as wnba

print("PWHL public:", [x for x in dir(pwhl) if not x.startswith("_")][:40])
print("WNBA public:", [x for x in dir(wnba) if not x.startswith("_")][:40])

for name in dir(pwhl):
    if "season" in name.lower() or "stat" in name.lower() or "player" in name.lower():
        obj = getattr(pwhl, name)
        if callable(obj):
            print("pwhl", name, inspect.signature(obj) if hasattr(inspect, "signature") else "")
