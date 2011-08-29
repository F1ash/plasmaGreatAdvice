DESTDIR=/usr
INSTALL=install -D -m 0644 -p
APP_NAME=kde-plasma-motivator
KAPPS=share/kde4/apps
KSERV=share/kde4/services
PLASMA=plasma/plasmoids
CODE=contents/code
ICONS=contents/icons

build:
	@echo "Nothing to build"

install: build
	$(INSTALL) metadata.desktop $(DESTDIR)/$(KSERV)/$(APP_NAME).desktop
	$(INSTALL) metadata.desktop $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/metadata.desktop
	$(INSTALL) $(CODE)/main.py $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/main.py
	$(INSTALL) $(CODE)/getText.sh $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/getText.sh
	$(INSTALL) $(ICONS)/advice.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/advice.png

clean:
	rm -rf $(DESTDIR)/$(KSERV)/$(APP_NAME).desktop
	rm -rf $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)
