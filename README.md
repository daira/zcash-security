Zcash security analysis
-----------------------

This repository contains code and documentation supporting security analysis of Zcash.

Contents:

* zcash-security.{[pdf](https://github.com/daira/zcash-security/raw/main/zcash-security.pdf),[odp](https://github.com/daira/zcash-security/raw/main/zcash-security.odp)}: slides for Daira's "Explaining the Security of Zcash" [presentation](https://www.youtube.com/watch?v=f6UToqiIdeY) at Zcon3.
* [sapling_entropy.py](sapling_entropy.py): calculate the entropy of ToScalar<sup>Sapling</sup>(PRF<sup>expand</sup><sub>K</sub>(constant))
  where K is 256 bits.

License
-------

All code and documentation in this repository is licensed under the [MIT license](LICENSE).
