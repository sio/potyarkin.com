title: Cirrus CI integration for GitLab projects
tags: automation, ci

[Cirrus CI] is a relatively new hosted CI service that offers several unique
features. It's probably the only CI provider to offer full virtualization
(KVM) or FreeBSD runners for free. Currently their business model is centered
around GitHub Marketplace and only the projects hosted at GitHub are
supported.

Fortunately Cirrus CI provides a very capable GraphQL [API]. Thanks to that I
was able to write a simple command line tool to trigger CI builds with custom
configuration: [cirrus-run]. It reads a local YAML file and executes Cirrus
CI build with that configuration. You can execute the build against any
GitHub repo you're allowed to access.

Since build configuration is not provided by the repo the job may have no
relation to it. You can execute any number of jobs for any number of projects
against a single dummy holding repo at GitHub - which is the approach I
suggest to use for setting up integration with other source code hosting
platforms.

Here is how I've set it up with GitLab:

  - Project repo is hosted at GitLab
  - Each push triggers a new build in GitLab CI
  - The only purpose of that build is to execute `cirrus-run`
  - [cirrus-run] triggers the real build in Cirrus CI, waits for it to
    complete and reports the results.

    Cirrus CI build is owned by a dummy GitHub repo that contains only one
    initial commit. Providing [custom clone script] allows to skip cloning
    that dummy repo.

That allows me to continue using GitLab to host my project and GitLab CI to
run the jobs it's good at while delegating the more demanding jobs to Cirrus
CI. All status reports are gathered by GitLab CI and failure notifications
arrive uniformly to my inbox regardless of where the build was executed.

[Cirrus CI]: https://cirrus-ci.org/
[custom clone script]: https://cirrus-ci.org/guide/tips-and-tricks/#custom-clone-command
[API]: https://cirrus-ci.org/api/
[cirrus-run]: https://github.com/sio/cirrus-run
