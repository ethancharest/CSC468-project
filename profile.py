import geni.portal as portal
import geni.rspec.pg as rspec

request = portal.context.makeRequestRSpec()

# Single XenVM node to host both Docker containers (Nginx frontend + Python backend)
node = request.XenVM("docker-host")

# Ubuntu 22.04 LTS - stable, well-supported for Docker
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"

# Allocate 2 vCPUs - sufficient for Nginx + Flask/FastAPI under light/moderate load
node.cores = 2

# Allocate 4GB RAM:
#   ~500MB  OS baseline
#   ~300MB  Docker daemon overhead
#   ~50MB   Nginx alpine container
#   ~250MB  Python slim + Flask/FastAPI container
#   ~900MB  Total expected usage
#   ~4GB    Allocated (headroom for future DB, cache, auth, monitoring)
node.ram = 4096  # MB

# Routable IP so you can access the frontend from a browser
node.routable_control_ip = "true"

# ---- Startup Commands ----

# Update package index
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt update"))

# Install Docker
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y docker.io"))

# Install Docker Compose (v2 plugin)
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y docker-compose-v2"))

# Enable and start Docker daemon
node.addService(rspec.Execute(shell="/bin/sh", command="sudo systemctl enable docker"))
node.addService(rspec.Execute(shell="/bin/sh", command="sudo systemctl start docker"))

# Add the default user to the docker group (avoids needing sudo for docker commands)
node.addService(rspec.Execute(shell="/bin/sh", command="sudo usermod -aG docker $USER"))

# Clone your project repository
node.addService(rspec.Execute(shell="/bin/sh", command="git clone https://github.com/ethancharest/CSC468-project.git /home/user/project"))

# Move into project directory and start services with Docker Compose
node.addService(rspec.Execute(shell="/bin/sh", command="cd /home/user/project && sudo docker compose up -d"))

# Verify both containers are running (output visible in CloudLab logs)
node.addService(rspec.Execute(shell="/bin/sh", command="sudo docker ps"))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
