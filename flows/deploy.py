from myFlow import etlFlow
from prefect.deployments import Deployment

from prefect.infrastructure.container import DockerContainer

docker_container_block = DockerContainer.load("my-first-flow")

docker_dep = Deployment.build_from_flow(
flow = etlFlow,
name = 'docker-flow',
infrastructure = docker_container_block
)

if __name__ == '__main__':
	docker_dep.apply()
