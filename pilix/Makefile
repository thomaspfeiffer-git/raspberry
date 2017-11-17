#############################################################################
# Makefile                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                 #
#############################################################################

LOGDIR=./Logs/
PICDIR=./Pictures/

.PHONY: clean run directories

clean:
	rm $(LOGDIR)/*
	rm $(PICDIR)/*

run: directories
	nohup ./Buttons.py >> $(LOGDIR)/buttons.log 2>>$(LOGDIR)/buttons.err &
	nohup ./Pilix.py >> $(LOGDIR)/pilix.log 2>>$(LOGDIR)/pilix.err &

directories:
	if [ ! -d $(LOGDIR) ]; then \
	   mkdir $(LOGDIR);         \
	fi
	if [ ! -d $(PICDIR) ]; then \
	   mkdir $(PICDIR);         \
	fi

# eof #

