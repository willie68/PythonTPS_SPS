package utils

import (
	"os"
	"path/filepath"
)

var temp = ""

func GetTempDir() (string, error) {
	if temp == "" {
		dname, err := os.MkdirTemp("", "pytps")
		if err != nil {
			return "", err
		}
		temp = dname
	}
	return temp, nil
}

func GetTempName(name string) (string, error) {
	d, err := GetTempDir()
	if err != nil {
		return "", err
	}
	return filepath.Join(d, name), nil
}
