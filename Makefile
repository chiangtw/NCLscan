ifeq ($(PREFIX),)
    export PREFIX = $(word 1, $(subst :, , $(PATH)))
endif

all: binary

binary:
	@cd bin; make

.PHONY: clean install uninstall

clean:
	@cd bin; make clean

install:
	@echo "Install NCLscan to $(PREFIX)"
	@cd bin; make install
	install NCLscan.py $(PREFIX)

uninstall:
	@cd bin; make uninstall
	@cd $(PREFIX); $(RM) NCLscan.py
