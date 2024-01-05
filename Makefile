all: dot png

SCRIPT	:= ism.py
OUTPUT	?= $(basename $(SCRIPT)).png
DOTFILE	?= dag_graph.dot
FOLDER	?= $(PWD)
T	?= dot
FLAGS	?=

ifneq ($(F),)
    FOLDER = $(F)
endif

ifneq ($(G),)
    FLAGS += -g $(G)
endif

ifeq ($(V),1)
FLAGS	+= -v
endif

dump: dot
	cat $(DOTFILE)

dot:
	./$(SCRIPT) $(FLAGS) $(FOLDER)

png: dot
	$(T) -Tpng $(DOTFILE) -o $(OUTPUT)

clean:
	rm *.png *.dot
