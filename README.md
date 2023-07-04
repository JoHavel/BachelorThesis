# Symbol synthesis evaluation

> This repository is forked from [Jirka-Mayer/BachelorThesis](https://github.com/Jirka-Mayer/BachelorThesis) and it is modified to run the same experiments with synthetic symbol images. To view its README, visit the link.


## Setting up on a fresh machine in a virtual environment

Create python virtual environment (even python 3.6 will do):

    python3 -m venv .venv

Activate the environment in your shell:

    source .venv/bin/activate

Upgrade pip in the venv:

    pip3 install --upgrade pip

Install all the necessary modules in the proper versions:

    pip3 install -r venv-requirements.txt

Download PRIMUS dataset (as a `.tgz` file) from
[https://grfia.dlsi.ua.es/primus/](https://grfia.dlsi.ua.es/primus/) into the `datasets` folder. It need not be extracted.

    wget -O ./datasets/primusCalvoRizoAppliedSciences2018.tgz https://grfia.dlsi.ua.es/primus/packages/primusCalvoRizoAppliedSciences2018.tgz

Download staff-removal set of CVC-MUSCIMA images from [http://www.cvc.uab.es/cvcmuscima/index_database.html](http://www.cvc.uab.es/cvcmuscima/index_database.html). And extract it.

    wget -O ./datasets/CVCMUSCIMA_SR.zip https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVCMUSCIMA_SR.zip
    mkdir -p datasets
    unzip datasets/CVCMUSCIMA_SR.zip -d datasets/cvc-muscima
    mv datasets/CvcMuscima-Distortions datasets/cvc-muscima

Download MUSCIMA++ from [https://ufal.mff.cuni.cz/muscima](https://ufal.mff.cuni.cz/muscima). And extract it.

    wget -O ./datasets/MUSCIMA-pp_v1.0.zip https://github.com/apacha/OMR-Datasets/releases/download/datasets/MUSCIMA-pp_v1.0.zip
    mkdir -p datasets/muscima-pp
    unzip datasets/MUSCIMA-pp_v1.0.zip -d datasets/muscima-pp

Copy `config_example.py` to `config.py` and modify if needed (most likely not).

    cp config_example.py config.py

Now you are ready to run the experiments and inspections.


## Adding custom symbols into the symbol repository

In [`mashcima/__init__.py`](mashcima/__init__.py) inside the constructor of the `Mashcima` class there's a final section, when there is a set of `assert` statements
that check that each symbol has at least one occurence. Before this block, you can insert your own code that modifies the symbol lists. Ideally by calling some helper functions defined in some other file.


### What symbols to modify and how

> The format is: symbol name - sprite name(s)

Single-sprite symbols with the origin in the geometric center of the image:

    WHOLE_NOTES - notehead
    QUARTER_RESTS - rest
    EIGHTH_RESTS - rest
    SIXTEENTH_RESTS - rest

Single-sprite accidentals with the origin in the center of the "eye" of the symbol:

    FLATS - /
    SHARPS - /
    NATURALS - /
    
    -> just sprites, not sprite groups so they have no name,
    but when added onto a Note, the sprite will be named "accidental"

Single-sprite symbols with the origin in the middle-top or middle-bottom:

    WHOLE_RESTS - rest
    HALF_RESTS - rest

Multi-sprite notehead-stem symbols with origin in the geometric center of the notehead:

    HALF_NOTES - notehead, stem
    QUARTER_NOTES - notehead, stem
    EIGHTH_NOTES - notehead, stem, flag_8
    SIXTEENTH_NOTES - notehead, stem, flag_16

    -> the sprite groups also have one special point, named "stem_head",
    which is just the x coordinate of the top-most pixel
    
All clefs have a single sprite with the origin in horizontal center and vertically aligned to the defining staffline. Getting the origin for G and F clefs is difficult so we will skip those, but we can get the origin for C clefs as it's the geometric center of the clef. So we will only synthesize C clefs, just like we do whole notes.

    G_CLEFS - clef
    F_CLEFS - clef
    C_CLEFS - clef

Symbols that need not be synthesized (too simple, too rare, no training data):

    LONGA_RESTS
    BREVE_RESTS
    DOTS
    LEDGER_LINES
    BAR_LINES
    TALL_BAR_LINES
    TIME_MARKS

The number of symbols for the default MUSCIMA++ extraction process is following:

    WHOLE_NOTES: 1183
    HALF_NOTES: 845
    QUARTER_NOTES: 15424
    EIGHTH_NOTES: 1697
    SIXTEENTH_NOTES: 334
    LONGA_RESTS: 8
    BREVE_RESTS: 12
    WHOLE_RESTS: 83
    HALF_RESTS: 166
    QUARTER_RESTS: 553
    EIGHTH_RESTS: 1058
    SIXTEENTH_RESTS: 426
    FLATS: 1064
    SHARPS: 1689
    NATURALS: 1021
    DOTS: 3181
    LEDGER_LINES: 6049
    BAR_LINES: 2226
    TALL_BAR_LINES: 633
    G_CLEFS: 341
    F_CLEFS: 250
    C_CLEFS: 155
    TIME_MARKS[time_0]: 1
    TIME_MARKS[time_1]: 1
    TIME_MARKS[time_2]: 28
    TIME_MARKS[time_3]: 64
    TIME_MARKS[time_4]: 98
    TIME_MARKS[time_5]: 6
    TIME_MARKS[time_6]: 17
    TIME_MARKS[time_7]: 6
    TIME_MARKS[time_8]: 23
    TIME_MARKS[time_9]: 1
    TIME_MARKS[time_c]: 26
