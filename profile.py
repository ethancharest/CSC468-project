import geni.portal as portal
import geni.rspec.pg as rspec

request = portal.context.makeRequestRSpec()

# Single XenVM node to host both Docker containers (Nginx frontend + Python backend)
node = request.XenVM("docker-host")

# Ubuntu 22.04 LTS - stable, well-supported for Docker
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"

# Allocate 2 vCPUs - sufficient for Nginx + Flask under light/moderate load
node.cores = 2

# Allocate 4GB RAM:
#   ~500MB  OS baseline
#   ~300MB  Docker daemon overhead
#   ~50MB   Nginx alpine container
#   ~250MB  Python slim + Flask container
#   ~900MB  Total expected usage
#   ~4GB    Allocated (headroom for future DB, cache, auth, monitoring)
node.ram = 4096  # MB

# Routable IP so you can access the frontend from a browser
node.routable_control_ip = "true"

# ---- Startup Commands ----
# All commands run as root via sudo, sequentially on the node after boot.

# Update package index
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt update -y"))

# Install Docker and Docker Compose v2 in one step
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y docker.io docker-compose-v2"))

# Enable and start Docker daemon
node.addService(rspec.Execute(shell="/bin/sh", command="sudo systemctl enable docker && sudo systemctl start docker"))

node.addService(rspec.Execute(shell="/bin/sh", command="whoami > /tmp/startup-user.txt && echo $HOME >> /tmp/startup-user.txt"))

# Clone the project repository into the default user's home directory
node.addService(rspec.Execute(shell="/bin/sh", command="git clone https://github.com/ethancharest/CSC468-project.git /users/$(whoami)/project"))

# Start both containers using absolute path to docker-compose.yml
node.addService(rspec.Execute(shell="/bin/sh", command="sudo docker compose -f /users/$(whoami)/project/docker-compose.yml up -d --build"))

# Verify both containers are running (output visible in CloudLab logs)
node.addService(rspec.Execute(shell="/bin/sh", command="sudo docker ps"))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
