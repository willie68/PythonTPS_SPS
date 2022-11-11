@echo off
go build -ldflags="-s -w" -o PyInstall.exe cmd/main.go