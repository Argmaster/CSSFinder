# Packaging

A Python Wheel is a built package format for Python that can be easily
installed and distributed, containing all the files necessary to install a
module and can be installed with pip with all dependencies automatically
installed too.

To create wheel of cssfinder use `poe` task in terminal:

```
poe build
```

![poe_build](https://user-images.githubusercontent.com/56170852/223251363-61fc4d00-68ad-429c-9fbb-8ab7f4712451.png)

This will create `dist/` directory with `cssfinder-0.7.0` or alike inside.

Wheel file can be installed with

```
pip install ./dist/cssfinder-0.7.0
```

What you expect is

```
Successfully installed cssfinder-0.7.0
```

or rather something like

```
Successfully installed click-8.1.3 contourpy-1.0.7 cssfinder-0.7.0 cycler-0.11.0 dnspython-2.3.0 email-validator-1.3.1 fonttools-4.39.0 idna-3.4 jsonref-1.1.0 kiwisolver-1.4.4 llvmlite-0.39.1 markdown-it-py-2.2.0 matplotlib-3.7.1 mdurl-0.1.2 numba-0.56.4 numpy-1.23.5 packaging-23.0 pandas-1.5.3 pendulum-2.1.2 pillow-9.4.0 pydantic-1.10.5 pygments-2.14.0 pyparsing-3.0.9 python-dateutil-2.8.2 pytz-2022.7.1 pytzdata-2020.1 rich-13.3.2 scipy-1.10.1 six-1.16.0 typing-extensions-4.5.0
```

But `cssfinder-0.7.0` should be included in this list.
