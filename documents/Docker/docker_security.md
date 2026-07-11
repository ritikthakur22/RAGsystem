# Docker Security Best Practices

When deploying containers, the security of the Docker host, the container images, and the runtime environment is paramount.

## 1. Keep Host and Docker Updated
Ensure the underlying host OS and the Docker engine are updated with the latest security patches.

## 2. Do Not Run Containers as Root
By default, Docker containers run as the root user. Always specify a non-root user in your Dockerfile using the `USER` instruction.
```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

## 3. Use Trusted and Minimal Base Images
- Prefer official images from Docker Hub.
- Use minimal images like Alpine Linux or distroless images to reduce the attack surface.
- Regularly scan images for vulnerabilities using tools like Trivy or Clair.

## 4. Limit Container Resources
Prevent Denial of Service (DoS) attacks by limiting memory and CPU usage per container.
```bash
docker run -m 512m --cpus 1.0 my-container
```

## 5. Avoid Privileged Containers
Never run a container with the `--privileged` flag unless absolutely necessary, as it gives the container almost full access to the host system.

## 6. Mount Filesystems as Read-Only
If a container does not need to write to its filesystem, mount it as read-only.
```bash
docker run --read-only my-container
```

## 7. Protect the Docker Daemon Socket
Do not expose the Docker daemon socket (`/var/run/docker.sock`) to containers or over the network without mutual TLS authentication. Any user with access to the Docker socket has root-level access to the host.
