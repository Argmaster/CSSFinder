# Profiling

To run simple profiling, You can use following command:

```
python -mcProfile -o "#examples_profile_5qubits_prof.prof" "assets/profiling/5qubits_prof/cssfproject.py"
```

Then You can view output using [snakeviz](https://pypi.org/project/snakeviz/):

```
snakeviz "#examples_profile_5qubits_prof.prof"
```
