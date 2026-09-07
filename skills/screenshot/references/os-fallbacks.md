# Direct OS capture fallbacks

## Direct OS commands (fallbacks)

Use these when you cannot run the helpers.

### macOS

- Full screen to a specific path:

```bash
screencapture -x output/screen.png
```

- Pixel region:

```bash
screencapture -x -R100,200,800,600 output/region.png
```

- Specific window id:

```bash
screencapture -x -l12345 output/window.png
```

- Interactive selection or window pick:

```bash
screencapture -x -i output/interactive.png
```

### Linux

- Full screen:

```bash
scrot output/screen.png
```

```bash
gnome-screenshot -f output/screen.png
```

```bash
import -window root output/screen.png
```

- Pixel region:

```bash
scrot -a 100,200,800,600 output/region.png
```

```bash
import -window root -crop 800x600+100+200 output/region.png
```

- Active window:

```bash
scrot -u output/window.png
```

```bash
gnome-screenshot -w -f output/window.png
```
