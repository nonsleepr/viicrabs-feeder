# SevenCrabs Feeder

A command-line utility to interact with [ElevenLabs
Reader](https://elevenlabs.io/text-reader).

## Motivation

A wonderful read-it-later app [Omnivore was acquired by
ElevenLabs](https://elevenlabs.io/blog/omnivore-joins-elevenlabs) and closed
shortly after.
While ElevenLabs text-to-speech tech is wonderful, their reader app lacks
useful features.

This little program aims to add make it easy to load articles into ElevenLabs
Reader straight from the command line allowing to do simple integrations.

## Usage

```bash
# Login
viicrabs login
# Add URL
viicrabs add https://elevenlabs.io/blog/omnivore-joins-elevenlabs
# Pipe input
cat article.txt | viicrabs add --title "My own article"
# Add file
viicrabs add ./another-article.txt
```

## Try It

```bash
uv run --with 'git+https://github.com/nonsleepr/viicrabs-feeder/' viicrabs --help
```

## Credentials

Currently only login/password flow without 2FA is supported.
When `viicrabs login` is run, credentials are saved into OS Keyring.
