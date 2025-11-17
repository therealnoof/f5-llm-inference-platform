# Building and Pushing Multi-Platform Docker Images

This guide explains how to build Docker images that work on both Apple Silicon (ARM64) and Intel/AMD (AMD64) systems.

## Why Multi-Platform?

If you build a Docker image on an Apple Silicon Mac, it will only work on ARM64 systems. To make it work on Linux servers (AMD64), you need to build a multi-platform image.

## Prerequisites

1. Docker Desktop installed and running
2. Docker Hub account
3. `docker buildx` enabled (included in Docker Desktop)

## One-Time Setup

### 1. Enable Docker Buildx

Docker buildx is included in Docker Desktop, but you may need to create a builder:

```bash
# Create a new builder instance
docker buildx create --name multiplatform --driver docker-container --use

# Bootstrap the builder
docker buildx inspect --bootstrap
```

### 2. Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
```

## Building Multi-Platform Images

### Method 1: Build and Push (Recommended)

Replace `YOUR_USERNAME` with your actual Docker Hub username:

```bash
cd ~/Claude/projects

# Build for both AMD64 and ARM64, and push directly to Docker Hub
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t YOUR_USERNAME/coffee-ai-guardrails:latest \
  --push \
  .
```

**Example:**
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t hd1912/coffee-ai-guardrails:latest \
  --push \
  .
```

### Method 2: Build with Version Tags

Build and tag with both `latest` and a version number:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t YOUR_USERNAME/coffee-ai-guardrails:latest \
  -t YOUR_USERNAME/coffee-ai-guardrails:v1.0 \
  --push \
  .
```

### Method 3: Build Locally (For Testing)

To build and load into local Docker (single platform only):

```bash
# For your current architecture only
docker buildx build \
  --platform linux/amd64 \
  -t YOUR_USERNAME/coffee-ai-guardrails:latest \
  --load \
  .
```

**Note:** `--load` only works with a single platform. Use `--push` for multi-platform.

## Verification

### Check Image Manifest

After pushing, verify the multi-platform manifest:

```bash
docker buildx imagetools inspect YOUR_USERNAME/coffee-ai-guardrails:latest
```

You should see output showing both platforms:
```
Name:      docker.io/YOUR_USERNAME/coffee-ai-guardrails:latest
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:...

Manifests:
  Name:      docker.io/YOUR_USERNAME/coffee-ai-guardrails:latest@sha256:...
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/amd64

  Name:      docker.io/YOUR_USERNAME/coffee-ai-guardrails:latest@sha256:...
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm64
```

## Complete Build and Push Workflow

Here's the complete process from start to finish:

```bash
# 1. Navigate to project
cd ~/Claude/projects

# 2. Ensure Docker is logged in
docker login

# 3. Create buildx builder (one-time setup)
docker buildx create --name multiplatform --driver docker-container --use
docker buildx inspect --bootstrap

# 4. Build and push multi-platform image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t YOUR_USERNAME/coffee-ai-guardrails:latest \
  --push \
  .

# 5. Verify the build
docker buildx imagetools inspect YOUR_USERNAME/coffee-ai-guardrails:latest
```

## Testing on Different Platforms

### On AMD64 Linux Server

```bash
docker pull YOUR_USERNAME/coffee-ai-guardrails:latest
docker run -p 8501:8501 YOUR_USERNAME/coffee-ai-guardrails:latest
```

### On Apple Silicon Mac

```bash
docker pull YOUR_USERNAME/coffee-ai-guardrails:latest
docker run -p 8501:8501 YOUR_USERNAME/coffee-ai-guardrails:latest
```

Docker will automatically pull the correct architecture for each platform.

## Updating Your Image

When you make changes to your app:

```bash
# 1. Make your code changes
# 2. Commit to git (optional)
git add .
git commit -m "Update app"

# 3. Rebuild and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t YOUR_USERNAME/coffee-ai-guardrails:latest \
  -t YOUR_USERNAME/coffee-ai-guardrails:v1.1 \
  --push \
  .
```

## Troubleshooting

### "docker buildx" command not found

Update Docker Desktop to the latest version.

### Builder instance not found

Create a new builder:
```bash
docker buildx create --name multiplatform --driver docker-container --use
```

### Build fails with "multiple platforms feature is currently not supported"

Make sure you're using the buildx builder:
```bash
docker buildx use multiplatform
```

### Cannot push to Docker Hub

Make sure you're logged in:
```bash
docker login
```

### Build is very slow

Multi-platform builds take longer because Docker builds for multiple architectures. The first build will be slow, but subsequent builds will use cache.

To speed up:
```bash
# Use BuildKit cache
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=YOUR_USERNAME/coffee-ai-guardrails:buildcache \
  --cache-to type=registry,ref=YOUR_USERNAME/coffee-ai-guardrails:buildcache,mode=max \
  -t YOUR_USERNAME/coffee-ai-guardrails:latest \
  --push \
  .
```

## Best Practices

1. **Always build for both platforms** when pushing to Docker Hub
2. **Use version tags** in addition to `latest` (e.g., v1.0, v1.1)
3. **Test locally** before pushing to Docker Hub
4. **Document your build process** in your repository
5. **Use buildx cache** for faster subsequent builds

## Quick Reference

```bash
# One-command build and push (most common)
docker buildx build --platform linux/amd64,linux/arm64 -t USERNAME/IMAGE:latest --push .

# Build with version tag
docker buildx build --platform linux/amd64,linux/arm64 -t USERNAME/IMAGE:latest -t USERNAME/IMAGE:v1.0 --push .

# Check what platforms an image supports
docker buildx imagetools inspect USERNAME/IMAGE:latest

# Test locally (single platform)
docker buildx build --platform linux/amd64 -t USERNAME/IMAGE:latest --load .
docker run -p 8501:8501 USERNAME/IMAGE:latest
```

## Additional Resources

- [Docker Buildx Documentation](https://docs.docker.com/buildx/working-with-buildx/)
- [Multi-platform Images](https://docs.docker.com/build/building/multi-platform/)
- [Docker Hub](https://hub.docker.com)
