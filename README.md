# Cache Simulator

based on https://github.com/caleb531/cache-simulator

## Example

```sh
# 3-way set associative (LRU; 2 words per block), address can be given in command line or `trace.out`
cache-simulator --cache-size 24 --num-blocks-per-set 3 --num-words-per-block 2 --word-addrs 3 180 43 2 191 88 190 14 181 44 186 253 --word-addrs-trace "trace.out"

# two level cache hierarchy
cache-simulator --l1-cache-size 24 --l1-num-blocks-per-set 3 --l1-num-words-per-block 2 --l1-word-addrs-trace "trace.out" --l1-write-miss-file "miss1.out" --two-level --l2-cache-size 64 --l2-num-blocks-per-set 2 --l2-num-words-per-block 32 --l2-write-miss-file "miss2.out"
```

## Installing

```
python3 setup.py install
```
