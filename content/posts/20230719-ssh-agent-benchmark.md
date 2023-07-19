title: Benchmarking ssh-agent performance
tags: ssh, cryptography, benchmark, go, ed25519
slug: ssh-agent-benchmark
date: 2023-07-19

I have an application idea that would require calling ssh-agent rather
frequently - but how many requests per second can it handle?

To answer this question I wrote a [small benchmark][benchmark] in Go.
It runs a tight loop sending messages for ssh-agent to sign.
Turns out the agent is pretty fast!

On a cheap cloud machine it was able to reliably sign more than 500 messages
per second with an ED25519 key. RSA signing was about 4-5 times slower, as
expected.
For a personal heuristic I've decided to remember that ED25519 signatures
cost 2ms and RSA ones 8ms.

Message size had little effect on throughput because both in ED25519 and in
RSA signatures inputs are hashed with a fast SHA algorithm prior to any other
processing.

Just in case my random number generator was too slow I checked if it affects
the benchmark results. Tests confirmed that it doesn't.

Of course, 500 rps does not sound _web scale_ but for me it's more than
enough. OpenSSH ssh-agent utilizes only a single CPU core, so there is some
potential for performance improvement if you need - but that would mean
doing the signatures in your software. I would rather trust OpenSSH team
(who are known to be just the right amount of paranoid) than touch private key
material with my clumsy hands.

---

You can run the same tests yourself: clone the [repo] and execute `make` from
top-level directory.
Benchmark names describe the key being used, message size and whether the
message is unique or the same for each iteration. Here is a sample output:

```console
BenchmarkSshAgent/key_ed25519/32B/unique-4          3553      1763363 ns/op
BenchmarkSshAgent/key_ed25519/32B/same-4            3568      1708270 ns/op
BenchmarkSshAgent/key_rsa4096/32B/unique-4           778      7824780 ns/op
BenchmarkSshAgent/key_rsa4096/32B/same-4             763      7657785 ns/op
BenchmarkSshAgent/key_ed25519/64B/unique-4          3456      1752457 ns/op
BenchmarkSshAgent/key_ed25519/64B/same-4            3598      1733750 ns/op
BenchmarkSshAgent/key_rsa4096/64B/unique-4           781      7639828 ns/op
BenchmarkSshAgent/key_rsa4096/64B/same-4             798      7720210 ns/op
BenchmarkSshAgent/key_ed25519/256B/unique-4         3549      1735906 ns/op
BenchmarkSshAgent/key_ed25519/256B/same-4           3417      1722301 ns/op
BenchmarkSshAgent/key_rsa4096/256B/unique-4          698      7738767 ns/op
BenchmarkSshAgent/key_rsa4096/256B/same-4            787      7625366 ns/op
BenchmarkSshAgent/key_ed25519/1024B/unique-4        3555      1703601 ns/op
BenchmarkSshAgent/key_ed25519/1024B/same-4          3651      1633226 ns/op
BenchmarkSshAgent/key_rsa4096/1024B/unique-4         805      7542115 ns/op
BenchmarkSshAgent/key_rsa4096/1024B/same-4           810      7437307 ns/op
BenchmarkSshAgent/key_ed25519/16384B/unique-4       3205      1935190 ns/op
BenchmarkSshAgent/key_ed25519/16384B/same-4         3296      1907921 ns/op
BenchmarkSshAgent/key_rsa4096/16384B/unique-4        783      7624776 ns/op
BenchmarkSshAgent/key_rsa4096/16384B/same-4          759      7620548 ns/op
```


[benchmark]: https://github.com/sio/ssh-agent-benchmark/blob/master/ssh_agent_test.go
[repo]: https://github.com/sio/ssh-agent-benchmark
