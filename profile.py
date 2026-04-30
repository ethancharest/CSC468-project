import geni.portal as portal
import geni.rspec.pg as rspec

request = portal.context.makeRequestRSpec()

node = request.XenVM('docker-host')

node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'

node.cores = 2

node.ram = 4096

node.routable_control_ip = 'true'

node.addService(rspec.Execute(shell='/bin/sh', command='sudo apt update -y'))
node.addService(rspec.Execute(shell='/bin/sh', command='sudo apt install -y docker.io docker-compose-v2'))
node.addService(rspec.Execute(shell='/bin/sh', command='sudo systemctl enable docker && sudo systemctl start docker'))
node.addService(rspec.Execute(shell='/bin/sh', command='git clone https://github.com/ethancharest/CSC468-project.git /users/geniuser/project'))
node.addService(rspec.Execute(shell='/bin/sh', command='echo "ENV=cloudlab" >> /users/geniuser/project/.env'))
node.addService(rspec.Execute(shell='/bin/sh', command='sudo docker compose -f /users/geniuser/project/docker-compose.yml up -d --build'))
node.addService(rspec.Execute(shell='/bin/sh', command='sudo docker ps'))

portal.context.printRequestRSpec()
