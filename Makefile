init:
	pip3 install -r requirements.txt

clean:
	pystarter clean

run: clean
	./variables.sh
	python3 run.py