title: Liberating effect of Ansible
date: 2018-06-26
tags: ansible, web, server, automation

Maintaining two or three Linux machines is not that hard of a task. For many
years I have thought it was not worth the effort to automate - regular backups
and version-controlled configuration files seemed to be just enough.

And then Ansible had blown my mind.

## History

It all started with a web server and a series of subpar hosting providers.
Setting that server up for the first time was an adventure. Repeating the setup
for the first relocation has given me a chance to introduce some improvements
but was otherwise uneventful. I started dreading the process when the need for
the third iteration had arisen. I was willing to put up with sluggishness and
several short downtimes just to delay the move to a new server. That was not OK.

Automating has clearly become a worthwhile task. I chose Ansible because it
doesn't require any special software on the controlled machines and because it
is mature enough to remain backwards compatible after updates. There are
numerous reviews of pros and cons of different configuration management systems,
but that's outside the scope of this article.

## Unexpected outcome

Ansible has definitely succeeded at the task I've thrown it at. That was
expected. What I couldn't foresee is how this experience would affect my
mindset - it was like a breath of fresh air! I have suddenly started to
understand why there exists all the buzz around *the cloud* and why cloud
service providers are dominating the market of virtual servers.

### Certainty

With my Ansible playbook I did not just automate the setup process, I created an
enforceable specification of what my server has to be like. At any time in the
future after executing the same playbook I can be certain that all configurable
parameters will be at the values I've defined.

Idempotent behavior allows me to run the playbook again and again without fear
of breaking anything. It should be noted though, that not all Ansible modules
are idempotent and one should always check the documentation before
incorporating a new module into the playbook.

### Immutability

There is even an option to take it one step further to truly [immutable
infrastructure] where any server can die at any point and no harm will be done.
This approach is for a bigger scale than a humble hobby project, though.

I have limited the immutability effort to a gentle reminder in /etc/motd and a
policy among administrators (me, myself and I) that no configuration changes are
to be made via shell connection.

### Disposability

Now it is incredibly easy for me to replicate that web server. It requires only
one command and a short coffee break. That means I can switch the hosting
provider at any moment I want. Choosing the hosting company has become a
non-issue: I invest only a minimal payment and no labor at all. If I don't like
what I get I'll be gone in no time.

Easy replication also means I can fire up another server for testing purposes,
then destroy it in a couple of hours and it will cost me only a few cents
because of hourly billing that most providers offer nowadays.

### Emotional detachment

Setting up a new server used to be somewhat similar to moving into a new
apartment.  First, there was scrupulous comparing of offers, after that a
dramatic moment of signing the lease and then the silent minutes alone in empty
apartment, staring at the walls. Each server was important and loved, breaking
or destroying it on purpose was unthinkable.

Now it's more like checking into a room at the hotel. And you get to be a
celebrity and send the rider list in advance, so that everything is set up to
your liking when you arrive. You can also check out at any moment without
worrying about the lease. There is no need to lug your favorite vimrc along
because you won't be editing anything there, in fact you'll hardly ever spend
any time logged in at all.

Randy Bias has summed this attitude in the [pets versus cattle] analogy. I think
it's quite on point even when you're managing a single machine, not the fleet of
servers.

### Infrastructure as code

And last, but not least, all you do with Ansible is automatically documented in
the playbook. You can use any version control system to track when any
particular change was introduced and why. That allows to revert the unwanted
changes as easily as was introducing them in the first place.

## Afterword

When you're outside the professional IT crowd it is not obvious that the cloud
infrastructure and the corresponding tools are within the reach of hobbyist
enthusiasts. But they are and they offer just as much value for personal
projects as they do in production environment.

If you find yourself tinkering with Linux administration more than once a week
it'll be worthwhile to try out Ansible or some other configuration management
tool.

[immutable infrastructure]: https://www.digitalocean.com/community/tutorials/what-is-immutable-infrastructure
[pets versus cattle]: http://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/

