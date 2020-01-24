title: Don't trust Docker for the selfhosted stuff

It is my strong belief that you shouldn't go crazy with _all-things-docker_
when deploying selfhosted services at home. Online forums, especially
[r/selfhosted], seem to foster an opinion that providing a `Dockerfile` or
better yet a `docker-compose.yml` or even prebuilt public images on Docker Hub
is an acceptable way to distribute software targeting the selfhosting crowd.

[r/selfhosted]: https://reddit.com/r/selfhosted/

I agree it is very convenient to deploy complex multipart services via these
tools. But the way many people appear to be doing that is a _security
nightmare_! Docker and Kubernetes are great tools that solve real world
problems but they need to be applied thoughfully after evaluating both their
strengths and their weaknesses.

