BUILD_DIR=build
FILE_NAME=plugin.video.sh_zingtv
CUR_DIR=$(FILE_NAME)
VERSION=0.0.2-35
OUTPUT=$(BUILD_DIR)/$(FILE_NAME)-$(VERSION).zip
EXCLUDES = */Makefile* *$(BUILD_DIR)/* *.pyc *venv/* *.git/* "*.gitignore*" "*_test.py"

all:
	mkdir -p $(BUILD_DIR)
	rm $(OUTPUT) -rf # force zip to create new file
	cd .. && zip -r $(CUR_DIR)/$(OUTPUT) $(CUR_DIR) -x $(EXCLUDES)
	cp $(OUTPUT) ~/www/repo/plugin.video.sh_zingtv/
