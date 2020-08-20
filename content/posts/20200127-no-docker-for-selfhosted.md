title: Don't blindly trust Docker for the selfhosted stuff
slug: no-docker-for-selfhosted
tags: docker, kubernetes, automation
date: 2020-01-27

It is my strong belief that you shouldn't go crazy with _all-things-docker_
when deploying selfhosted services at home. Online forums, especially
[r/selfhosted], seem to foster an opinion that providing a `Dockerfile` or
better yet a `docker-compose.yml` or even prebuilt public images on Docker Hub
is an acceptable way to distribute software targeting the selfhosting crowd.

[r/selfhosted]: https://reddit.com/r/selfhosted/

I agree it is very convenient to deploy complex multipart services via these
tools. But the way many people appear to be doing that is a security
nightmare! This is how we get to encounter [Heartbleed in the
wild][heartbleed] four years after it should've been extinct.

[heartbleed]: https://www.computerweekly.com/news/252437100/Heartbleed-and-WannaCry-thriving-in-Docker-community

There are [many][security-docs] comprehensive [writeups][security-101] on
Docker/Kubernetes security, I will highlight only a subset of problems below.

[security-docs]: https://kubernetes.io/docs/tasks/administer-cluster/securing-a-cluster/#protecting-cluster-components-from-compromise
[security-101]: https://www.stackrox.com/post/2019/07/kubernetes-security-101/

  - **Shared libraries**

    Running each service in its separate container results in having a
    separate set of shared libraries for each one of those services. It is
    convenient when you need to provide multiple incompatible dependencies at
    once, but that way the burden of tracking the state of all those
    dependencies lies on the user. Host OS can not tell you that one of the
    containers still ships a vulnerable version of some critical library -
    it's up to you to monitor and fix that.

  - **Container rebuilding**

    Fixing anything related to the container requires rebuilding the image.
    When you're using images from public registries you can not initiate image
    rebuild even when you know it's needed. Your best option is to contact the
    original uploader and to convince them to rebuild. That may take
    significant time during which the containers running that image remain
    vulnerable.

  - **Images from untrusted sources**

    In addition to the points above you put enormous amount of trust into
    people who provide the container you're running. In containerless scenario
    you're required to trust the vendor who provides the base OS and the
    developer who provides the custom applications you run upon that OS. When
    containers come into play, you must extend your trust to the maintainer of
    the container image, to the vendors who provide the base image that image
    is built upon, to all the developers who provide any piece of code
    included into that container. It does not even require malicious intent to
    introduce a vulnerability into the resulting container, simple
    incompetence of any of the parties involved may be just enough.

This is why containerizing any workload comes with a significant extra cost of
designing and automating security maintenance procedures. It is easy to skip
this step when you're a hobbyist - but that's just burying your head in the
sand and waiting for some script kiddie or botnet to hijack your network.

Here is a rough overview of the required overhead:

- You need to run only containers that are based on the images you've built
  yourself. This is the only way you can ensure swift rebuilding in case one
  of the base images provides a security update. This step may include running
  your own image registry and build service.
- You need to audit every Dockerfile you intend to build. This can only be
  done manually. And you need to check all the base images in the chain up to
  either a `FROM scratch` stanza or to a base image from trusted list.
- You need to maintain a list of trusted base images that come from vendors
  with good reputation in regards to handling security issues.
- You need to blacklist any image that does not come either from a trusted
  list or from a Dockerfile you've audited yourself.
- You need to setup automated image rebuilds and container rollouts:
    a) on schedule
    b) on any update in the base image dependency chain
- You need to setup automated vulnerability monitoring for the images you're
  running. This will require a lot more effort than subscribing to RSS feed of
  your distro security announcements - as it would've been the case with
  containerless deployment.

Add that on top of usual container orchestration chores - and bare metal
suddenly becomes attractive. Docker and Kubernetes are great tools that solve
real world problems but using them in a secure manner requires continuous
dedicated effort. For enterprise deployments the benefits of containerization
usually outweigh the extra maintenance cost, but for hobbyist use I'm not so
sure.
