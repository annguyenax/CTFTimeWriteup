@echo off
cd /d "D:\download\ctf-scratch\ptit26_winux"
del /q winux.state 2>nul
winux.exe < root_in.txt > root_out.txt 2>&1
