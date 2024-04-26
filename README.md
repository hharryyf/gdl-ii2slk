# gdl-ii2slk
A converter from grounded GDL-II (in ASP-format) to ISPL SLK

To translate a GDL-II to ISPL interpreted system run:

```
python translate-noterminal-v5.py [path to GDL-II file] [recall depth] > model.slk

```

To perform model checking run:
```
./mcmas-slk_64 [path to the ispl/slk file]

```

