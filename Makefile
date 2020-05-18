push: build
	docker push frankkkkk/k8s-nodeselector-during-execution:latest

build:
	docker build -t frankkkkk/k8s-nodeselector-during-execution:latest .

