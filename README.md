## fuelmats: Python-automated creation of MCNP fuel material cards

Patrick Park | <ppark@reed.edu> | Physics '22 | Reed College

### Scope

This project involves a python wrapper (`fuelmats.py`) that:
1. calculates number fractions of uranium fuel isotopes from the Core Burnup History Excel files
2. prints MCNP material cards (`results.txt`)

### Procedure

Essentially, we want to create MCNP materials cards with the following pseudocode syntax:
```
m{fe id} 92235.80c -{g U-235}  92238.80c 4.7999E-04
         40000.80c 4.6088E-04   1001.80c 1.6407E-02
c
mt{fe id} h/zr.10t zr/h.10t
```
Note that the negative value indicates mass fraction. A positive value indicates atom fraction. 

### Technical Notes
The TRIGA fuel elements contain uranium as a fine metallic dispersion in a ZrH matrix.

#### To-do Improvements

