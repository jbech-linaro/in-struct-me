all: dot

SCRIPT	:= ism.py
O	?= $(basename $(SCRIPT)).png
DOTFILE	?= dag_graph.dot
FOLDER	?= $(PWD)
T	?= dot
FLAGS	?= -o $(O) -c $(T)

ifneq ($(F),)
FOLDER = $(F)
endif

ifneq ($(G),)
FLAGS += -g $(G)
endif

ifneq ($(I),)
FLAGS += -i $(I)
endif

ifeq ($(V),1)
FLAGS	+= -v
endif

dump: dot
	cat $(DOTFILE)

.PHONY: dot
dot:
	./$(SCRIPT) $(FLAGS) $(FOLDER)

png:
	$(T) -Tpng $(DOTFILE) -o $(O)

clean:
	rm *.png *.dot
