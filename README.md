#### Usage

1. `gcc -O3 -march=native -mtune=native rand-branch.c -o rand-branch`
2. `sudo perf record -b -e cycles ./rand-bench`
3. `sudo perf script -F brstack > file.txt`
    - See `perf script -h` for more. Particularly `perf script -F brstackins --xed`
    - See also `perf report -h` and `perf annotate -h`
4. `parse-perf-data.py -f file.txt`

