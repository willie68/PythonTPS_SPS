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
	"strings"

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
		fmt.Printf("Is \"%s\" this the raspberry pi pico drive? [Y/n]:", drive)
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
	log.Infof("config loaded: %v", config.Config.Json())

	err = downloadNeededFiles()
	if err != nil {
		exit("can't download needed files: %v", err)
	}
	// if no src given
	//   download the needed files
	// checking the files
	// copy circuitpython uf2 file to mcu
	// wait til reset
	// checking for the circuit python drive
	// copy the application
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
		config.Co
		nfig.Firmware = tf
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
