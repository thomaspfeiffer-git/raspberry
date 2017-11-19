#############################################################################
# Makefile                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                 #
#############################################################################

LOGDIR=./Logs/
PICDIR=./Pictures/

.PHONY: clean run directories watchdog

run: directories watchdog
	nohup ./Buttons.py >> $(LOGDIR)/buttons.log 2>>$(LOGDIR)/buttons.err &
	nohup ./Pilix.py $(autostart) >> $(LOGDIR)/pilix.log 2>>$(LOGDIR)/pilix.err &

clean:
	rm -f $(LOGDIR)/*
	rm -f $(PICDIR)/*

directories:
	if [ ! -d $(LOGDIR) ]; then \
	   mkdir $(LOGDIR);         \
	fi
	if [ ! -d $(PICDIR) ]; then \
	   mkdir $(PICDIR);         \
	fi

watchdog:
	sudo modprobe bcm2835_wdt

keepalive:
	( while [ 1 ] ; do sudo bash -c "echo 'hi' > /dev/watchdog" ; sleep 1 ; done ) &


# eof #

