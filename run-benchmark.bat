@echo off

for /f %%d in ('dir /b .') do (
	if exist %%d\NUL (
		echo Running benchmark from %%d
		cd %%d
		exec.bat
		cd ..
	)
)