@echo off
for /l %%x in (1, 1, 1000) do (
	echo|set /p="Run number %%x... "
	python py_native_vtk_benchmark.py
	echo Done.
)