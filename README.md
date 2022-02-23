# OpenSAFELY Research Action

This repo provides a GitHub Action for verifying that
[OpenSAFELY](https://docs.opensafely.org/) research repos can run
correctly.

It is written as a "[composite run steps][1]" action.


## Usage

You can invoke this action from a Github workflow file (e.g.
`.github/workflows/opensafely_tests.yaml`) like so:

```yaml
name: Test that the project pipeline runs using dummy data

on: [push, workflow_dispatch]
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: opensafely-core/research-action@v2
```

The [research-template][2] repo includes such a [workflow file][3] already.


## Tests

Github actions are very difficult to test locally. The approach we use is to a)
lint locally using https://github.com/rhysd/actionlint and b) use Github as our
test runner, effectively doing integration tests.

So, to test, you need to first run lint:

    make lint

When ready, commit and push your changes to github, which will run the
integration test suite in parallel. If you have the gh cli installed, you can
check on the state of the test run:

    gh pr status


## Releasing a new version

Existing workflow files reference this repo using the `v2` tag. If you make
backwards compatible changes to this repo you'll need to update the
`v2` tag:

    `make tag-release`

Breaking changes should use a new version tag so that tests for existing
repos continue to pass.


[1]: https://docs.github.com/en/actions/creating-actions/creating-a-composite-run-steps-action
[2]: https://github.com/opensafely/research-template
[3]: https://github.com/opensafely/research-template/blob/main/.github/workflows/test_runner.yaml
