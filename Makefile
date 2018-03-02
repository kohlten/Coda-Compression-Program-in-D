CC=ldc2

.PHONY: all

all:
	dub build --compiler=$(CC) --build=release

.PHONY: allv

allv:
	dub build --compiler=$(CC) -v --build=release

.PHONY: clean

clean:
	dub clean

.PHONY: fclean

fclean:
	make clean
	rm bin/coda
	
.PHONY: install

install:
	sudo cp bin/coda /usr/bin
	
.PHONY: uninstall

uninstall:
	sudo rm usr/bin/coda

.PHONY: installWindows	

installWindows:
	mkdir C:/Program\ Files/coda
	copy bin/coda C:/Program\ Files/coda/

.PHONY: uninstallWindows

uninstallWindows:
	del C:/Program\ Files/coda/coda
	rmdir C:/Program\ Files/coda