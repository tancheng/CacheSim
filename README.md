# Cache Simulator

## Example

```sh
# 3-way set associative (LRU; 2 words per block), address can be given in command line or `trace.out`
cache-simulator --cache-size 24 --num-blocks-per-set 3 --num-words-per-block 2 --word-addrs 3 180 43 2 191 88 190 14 181 44 186 253 --word-addrs-trace "trace.out"
```

## Installing

```
python3 setup.py install
```
