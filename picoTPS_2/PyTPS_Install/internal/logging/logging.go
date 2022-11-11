package logging

import (
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	"gopkg.in/natefinch/lumberjack.v2"
)

const (
	LvlDebug = "DEBUG"
	LvlInfo  = "INFO"
	LvlAlert = "ALERT"
	LvlError = "ERROR"
	LvlFatal = "FATAL"
)

var Levels = []string{LvlDebug, LvlInfo, LvlAlert, LvlError, LvlFatal}

/*
ServiceLogger main type for logging
*/
type serviceLogger struct {
	Level     string
	LevelInt  int
	SystemID  string
	Attrs     map[string]interface{}
	Filename  string
	LvlPrefix bool
}

// Logger to use for all logging
var Logger = serviceLogger{
	LvlPrefix: false,
}

func init() {
	log.SetPrefix("")
	log.SetFlags(0)
}

// convinient methods
func SetLevel(level string) {
	Logger.SetLevel(level)
}

/*
Debug log this message at debug level
*/
func Debug(msg string) {
	Logger.Debug(msg)
}

/*
Debugf log this message at debug level with formatting
*/
func Debugf(format string, va ...interface{}) {
	Logger.Debugf(format, va)
}

/*
Info log this message at info level
*/
func Info(msg string) {
	Logger.Info(msg)
}

/*
Infof log this message at info level with formatting
*/
func Infof(format string, va ...interface{}) {
	Logger.Infof(format, va)
}

/*
Alert log this message at alert level
*/
func Alert(msg string) {
	Logger.Alert(msg)
}

/*
Alertf log this message at alert level with formatting.
*/
func Alertf(format string, va ...interface{}) {
	Logger.Alertf(format, va)
}

// Fatal logs a message at level Fatal on the standard logger.
func Fatal(msg string) {
	Logger.Fatal(msg)
}

// Fatalf logs a message at level Fatal on the standard logger with formatting.
func Fatalf(format string, va ...interface{}) {
	Logger.Fatalf(format, va)
}

// Error logs a message at level Error on the standard logger.
func Error(msg string) {
	Logger.Error(msg)
}

// Errorf logs a message at level Error on the standard logger with formatting.
func Errorf(format string, va ...interface{}) {
	Logger.Errorf(format, va)
}

/*
Init initialise logging
*/
func (s *serviceLogger) Init() {
	var w io.Writer
	if s.Filename == "" {
		w = os.Stdout
	} else {
		w = io.MultiWriter(&lumberjack.Logger{
			Filename:   s.Filename,
			MaxSize:    100, // megabytes
			MaxBackups: 3,
			MaxAge:     28,    //days
			Compress:   false, // disabled by default
		}, os.Stdout)
	}
	log.SetOutput(w)
}

func (s *serviceLogger) SetLevel(level string) {
	switch strings.ToUpper(level) {
	case LvlDebug:
		s.LevelInt = 0
	case LvlInfo:
		s.LevelInt = 1
	case LvlAlert:
		s.LevelInt = 2
	case LvlError:
		s.LevelInt = 3
	case LvlFatal:
		s.LevelInt = 4
	}
}

/*
Debug log this message at debug level
*/
func (s *serviceLogger) Debug(msg string) {
	if s.LevelInt <= 0 {
		if s.LvlPrefix {
			log.Printf("Debug: %s\n", msg)
		} else {
			log.Printf("%s\n", msg)
		}
	}
}

/*
Debugf log this message at debug level with formatting
*/
func (s *serviceLogger) Debugf(format string, va ...interface{}) {
	if s.LevelInt <= 0 {
		if s.LvlPrefix {
			log.Printf("Debug: %s\n", fmt.Sprintf(format, va...))
		} else {
			log.Printf("%s\n", fmt.Sprintf(format, va...))
		}
	}
}

/*
Info log this message at info level
*/
func (s *serviceLogger) Info(msg string) {
	if s.LevelInt <= 1 {
		if s.LvlPrefix {
			log.Printf("Info: %s\n", msg)
		} else {
			log.Printf("%s\n", msg)
		}
	}
}

/*
Infof log this message at info level with formatting
*/
func (s *serviceLogger) Infof(format string, va ...interface{}) {
	if s.LevelInt <= 1 {
		if s.LvlPrefix {
			log.Printf("Info: %s\n", fmt.Sprintf(format, va...))
		} else {
			log.Printf("%s\n", fmt.Sprintf(format, va...))
		}
	}
}

/*
Alert log this message at alert level
*/
func (s *serviceLogger) Alert(msg string) {
	if s.LevelInt <= 2 {
		if s.LvlPrefix {
			log.Printf("Alert: %s\n", msg)
		} else {
			log.Printf("%s\n", msg)
		}
	}
}

/*
Alertf log this message at alert level with formatting.
*/
func (s *serviceLogger) Alertf(format string, va ...interface{}) {
	if s.LevelInt <= 2 {
		if s.LvlPrefix {
			log.Printf("Alert: %s\n", fmt.Sprintf(format, va...))
		} else {
			log.Printf("%s\n", fmt.Sprintf(format, va...))
		}
	}
}

// Fatal logs a message at level Fatal on the standard logger.
func (s *serviceLogger) Fatal(msg string) {
	if s.LevelInt <= 4 {
		if s.LvlPrefix {
			log.Fatalf("Fatal: %s\n", msg)
		} else {
			log.Fatalf("%s\n", msg)
		}
	}
}

// Fatalf logs a message at level Fatal on the standard logger with formatting.
func (s *serviceLogger) Fatalf(format string, va ...interface{}) {
	if s.LevelInt <= 4 {
		if s.LvlPrefix {
			log.Fatalf("Fatal: %s\n", fmt.Sprintf(format, va...))
		} else {
			log.Fatalf("%s\n", fmt.Sprintf(format, va...))
		}
	}
}

// Error logs a message at level Error on the standard logger.
func (s *serviceLogger) Error(msg string) {
	if s.LevelInt <= 3 {
		if s.LvlPrefix {
			log.Printf("Error: %s\n", msg)
		} else {
			log.Printf("%s\n", msg)
		}
	}
}

// Errorf logs a message at level Error on the standard logger with formatting.
func (s *serviceLogger) Errorf(format string, va ...interface{}) {
	if s.LevelInt <= 3 {
		if s.LvlPrefix {
			log.Printf("Error: %s\n", fmt.Sprintf(format, va...))
		} else {
			log.Printf("%s\n", fmt.Sprintf(format, va...))
		}
	}
}

/*
Close this logging client
*/
func (s *serviceLogger) Close() {
}
