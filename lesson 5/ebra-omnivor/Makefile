all: case-tjaer-8

case-%:
	rm -rf sim_case1-$*/pdat/*
	xterm -e "python case1.py $*"&
postpro-%:
	paraview --data-directory=sim_case1-$*/pdat/
