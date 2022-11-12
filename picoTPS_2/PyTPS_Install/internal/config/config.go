package config

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"

	"gopkg.in/yaml.v3"
)

type config struct {
	Installer string
	Firmware  string            `yaml:"firmware"`
	Wipeware  string            `yaml:"wipeware"`
	Tps       map[string]string `yaml:"tps"`
}

var Config = config{}
var File string

func init() {
	Config.Installer = "https://raw.githubusercontent.com/willie68/PythonTPS_SPS/master/installer/installer.yaml"
}

func (c *config) Json() string {
	b, _ := json.Marshal(c)
	return string(b)
}

// Load loads the config
func Load(myFile string) error {
	if myFile == "" {
		return loadFromDefault()
	}
	File = myFile
	_, err := os.Stat(myFile)
	if err != nil {
		return err
	}
	data, err := ioutil.ReadFile(File)
	if err != nil {
		return fmt.Errorf("can't load config file: %s", err.Error())
	}
	dataStr := os.ExpandEnv(string(data))
	err = yaml.Unmarshal([]byte(dataStr), &Config)
	if err != nil {
		return fmt.Errorf("can't unmarshal config file: %s", err.Error())
	}
	return nil
}

func loadFromDefault() error {
	resp, err := http.Get(Config.Installer)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	dataStr, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	err = yaml.Unmarshal(dataStr, &Config)
	if err != nil {
		return fmt.Errorf("can't unmarshal config file: %s", err.Error())
	}
	return nil
}
