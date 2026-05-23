# gdl-ii2slk
A converter from **grounded** GDL-II (in ASP-format) to ISPL SLK. The [paper](https://proceedings.kr.org/2024/40/kr2024-0040-he-et-al.pdf) is attached 

Input assumption:

1) the GDL-II description is valid

2) all static variables only appear as facts (i.e., they are grounded away from the body of rules)

3) goal only appear in the head, role only appear as facts

Note that 2) and 3) are introduced for performance reasons

To translate a GDL-II to ISPL interpreted system run:

```
python translate-noterminal-v6.py [path to GDL-II file] [recall depth] > model.slk

```

You can then fill the formulas you want to model-checked against in the .slk file.

To perform model checking run:
```
./mcmas-slk_64 [path to the ispl/slk file]

```

To reproduce the experiments, just run:

```
./mcmas-slk_64 prisoner-v2/prisoner-v2-0.slk

./mcmas-slk_64 number/number-5-0-1.slk

./mcmas-slk_64 number/number-6-0-1.slk

./mcmas-slk_64 number/number-7-0-5.slk

./mcmas-slk_64 number/number-8-0-1.slk

```