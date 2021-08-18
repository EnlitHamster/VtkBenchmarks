@echo off
for /l %%x in (1, 1, 1000) do (
	echo|set /p="Run number %%x... "
	start /wait /min PythonEmbedding.exe
	echo Done.
)