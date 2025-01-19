# gdl-ii2slk
A converter from **grounded** GDL-II (in ASP-format) to ISPL SLK. The [paper](https://proceedings.kr.org/2024/40/kr2024-0040-he-et-al.pdf) is attached 

Input assumption:

1) the GDL-II description is valid

2) all static variables only appear as facts (i.e., they are grounded away from the body of rules)

3) goal only appear in the head, role only appear as facts

Note that 2) and 3) are introduced for performance reasons

To translate a GDL-II to ISPL interpreted system run:

```
python translate-noterminal-v5.py [path to GDL-II file] [recall depth] > model.slk

```

To perform model checking run:
```
./mcmas-slk_64 [path to the ispl/slk file]

```

