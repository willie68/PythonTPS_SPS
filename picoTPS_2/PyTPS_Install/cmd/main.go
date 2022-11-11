package main

import (
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"path"
	"path/filepath"
	"strings"
	"time"

	"github.com/willie68/PythonTPS_SPS/picoTPS_2/PyTPS_Install/internal/config"
	"github.com/willie68/PythonTPS_SPS/picoTPS_2/PyTPS_Install/internal/utils"

	log "github.com/willie68/PythonTPS_SPS/picoTPS_2/PyTPS_Install/internal/logging"

	flag "github.com/spf13/pflag"
)

var (
	drive string
	src   string
)

func init() {
	// variables for parameter override
	log.Logger.Info("init PyTPS Install")
	flag.StringVarP(&drive, "drive", "d", "", "drive of the Raspberry Pi Pico.")
	flag.StringVarP(&src, "src", "s", "", "where to find the needed files. Default: internet download")
}

func main() {
	flag.Parse()

	var err error
	var input string
	// if no drive given
	if drive == "" {
		//   selecting the right drive
		drive, err = selectDrive()
		if err != nil {
			log.Errorf("drive can't be selected automatically: %v", err)
		}
		log.Infof("found drive \"%s\" as pico drive", drive)
		fmt.Printf("Is \"%s\" the raspberry pi pico drive? [Y/n]:", drive)
		fmt.Scanln(&input)
		if (strings.ToLower(input) != "y") && (input != "") {
			fmt.Print("Input drive letter [type . for exit]:")
			fmt.Scanln(&input)
			if input != "." {
				drive = fmt.Sprintf("%s:", input)
			}
		}
		if input == "." {
			exit("user exit on drive select")
		}
	}
	// checking the drive
	driveok := false
	for !driveok {
		err = checkDrive(drive)
		if err != nil {
			log.Errorf("error on reading dir: %v", err)
			fmt.Print("Input drive letter [type . for exit]:")
			fmt.Scanln(&input)
			if input == "." {
				exit("user exit on drive select")
			}
			drive = fmt.Sprintf("%s:", input)
		} else {
			driveok = true
		}
	}
	err = config.Load(src)
	if err != nil {
		exit("can't load config file \"%s\": %v", src, err)
	}
	log.Info("installer script loaded")

	err = downloadNeededFiles()
	if err != nil {
		exit("can't download needed files: %v", err)
	}
	// if no src given
	//   download the needed files
	// checking the files
	// copy circuitpython uf2 file to mcu
	err = copyFirmware()
	if err != nil {
		exit("can't copy firware file: %v", err)
	}
	// wait til reset
	log.Info("waiting some seconds for pico to reboot")
	time.Sleep(5 * time.Second)
	fmt.Printf("Is \"%s\" the circuit drive? [Y/n]:", drive)
	input = ""
	fmt.Scanln(&input)
	if (strings.ToLower(input) != "y") && (input != "") {
		fmt.Print("Input drive letter [type . for exit]:")
		fmt.Scanln(&input)
		if input != "." {
			drive = fmt.Sprintf("%s:", input)
		}
	}
	if input == "." {
		exit("user exit on drive select")
	}
	// checking for the circuit python drive
	// copy the application
	err = copyTPSFiles()
	if err != nil {
		exit("can't copy firware file: %v", err)
	}
	log.Info("to start the tps, please reset the pico!")
	// try restart
	removeTempData()
	// finished
	log.Info("PyTPS successfully installed")
}

func selectDrive() (string, error) {
	return "C:", nil
}

func checkDrive(drive string) error {
	found := false
	files, err := ioutil.ReadDir(drive + "\\")
	if err != nil {
		return err
	}
	for _, n := range files {
		if strings.ToUpper(n.Name()) == "INFO_UF2.TXT" {
			found = true
		}
	}
	if found {
		return nil
	}
	return errors.New("drive seems not to be an raspberry pi pico drive. Do you restart the pico with bootsel pressed?")
}

func downloadNeededFiles() error {
	if IsUrl(config.Config.Firmware) {
		tf, err := utils.GetTempName(path.Base(config.Config.Firmware))
		if err != nil {
			return err
		}
		Download(config.Config.Firmware, tf)
		config.Config.Firmware = tf
	}
	for k, v := range config.Config.Tps {
		if IsUrl(v) {
			tf, err := utils.GetTempName(path.Base(v))
			if err != nil {
				return err
			}
			Download(v, tf)
			config.Config.Tps[k] = tf
		}
	}
	return nil
}

func Download(src string, file string) error {
	resp, err := http.Get(src)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	out, err := os.Create(file)
	if err != nil {
		return err
	}
	defer out.Close()
	defer resp.Body.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}

func IsUrl(str string) bool {
	u, err := url.Parse(str)
	return err == nil && u.Scheme != "" && u.Host != ""
}

func removeTempData() {
	temp, _ := utils.GetTempDir()
	os.RemoveAll(temp)
}

func exit(format string, a ...any) {
	if len(a) == 0 {
		log.Info(format + ". Exit.")
	} else {
		log.Info(fmt.Sprintf(format, a) + ". Exit.")
	}
	os.Exit(1)
}

func copyFirmware() error {
	base := path.Base(filepath.ToSlash(config.Config.Firmware))
	log.Infof("copy file %s", base)
	file := filepath.Join(drive, base)

	in, err := os.Open(config.Config.Firmware)
	if err != nil {
		return err
	}
	defer in.Close()

	out, err := os.Create(file)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, in)
	return err
}

func copyTPSFiles() error {
	for k, v := range config.Config.Tps {
		log.Infof("copy file %s", k)
		file := filepath.Join(drive, k)

		in, err := os.Open(v)
		if err != nil {
			return err
		}
		defer in.Close()

		out, err := os.Create(file)
		if err != nil {
			return err
		}
		defer out.Close()

		_, err = io.Copy(out, in)
		if err != nil {
			return err
		}
	}
	return nil
}
