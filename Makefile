DESTDIR=/usr
INSTALL=install -D -m 0644 -p
APP_NAME=kde-plasma-motivator
PLASMA=plasma/plasmoids

install: build
	$(INSTALL) metadata.desktop $(DESTDIR)/share/kde4/services/$(APP_NAME).desktop
	$(INSTALL) contents/code/main.py $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/code/main.py
	$(INSTALL) contents/code/getText.sh $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/code/getText.sh
	$(INSTALL) contents/icons/advice.png $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/icons/advice.png

clean:
	rm -rf $(DESTDIR)/share/kde4/services/$(APP_NAME).desktop
	rm -rf $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)
