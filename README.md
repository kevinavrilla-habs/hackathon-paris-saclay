# HABS Hackathon — team template

You change `process.py`. You push. Your code runs on HABS compute against the
full dataset, and the results come back to this repo's Actions page.

## Setup, once

**1. Make this repo yours.** Click *Use this template*. Call it anything.

**2. Send HABS your repo address** — `your-name/your-repo`, exactly as it
appears in the URL. We can only authorise a repo we know the name of, so
nothing works until you do this. You get **two things** back:

| | What it is | Where it goes |
| --- | --- | --- |
| **Team key** | one line, `xxxxxxxx-xxxx-…` | into the workflow, step 3 |
| **Results link** | a long `https://…` | keep it; it is how you read your files |

Tell us too if you later rename the repo, move it to another account, or work
on a branch other than `main` — each of those changes what GitHub signs, and
your pushes stop being recognised until we re-authorise them.

**3. Paste the key.** Open `.github/workflows/submit.yml` and replace
`PASTE-YOUR-TEAM-KEY-HERE`, keeping the quotes. Commit.

```yaml
HABS_KEY: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

That is the whole setup. The key is **not a password** — it only works from
your repository, on your `main` branch. GitHub vouches for that, and Azure
trusts GitHub. Nobody who copies it can do anything with it.

The **results link** is different: that one *is* a credential. Keep it out of
the repo, out of the workflow and out of screenshots.

**4. Push.** Open the **Actions** tab and watch your job run.

## The contract

```python
def process(data_dir: Path, out_dir: Path) -> None:
```

We call this once.

| | |
| --- | --- |
| `data_dir` | the dataset, **read-only**, identical for every team |
| `out_dir` | starts empty; everything you write here is kept and is yours |
| `$HABS_SCRATCH` | fast local disk for intermediates, **wiped** when the job ends |

Put your dependencies in `requirements.txt`. The image already has CUDA and
PyTorch, so don't install torch.

## Submitting

`git push`. That is the submission.

Open the **Actions** tab and your run is there, in two steps:

| | What it is doing | Usually |
| --- | --- | --- |
| **build your image** | installing your `requirements.txt` into a container | 1–2 min |
| **run on a GPU** | waiting its turn, then running `process()` on an H100 | minutes to an hour |

The split is there so the two ways a push can go wrong look different:

- **build is red** → your `requirements.txt`. A misspelt package, or a version
  with no build for Python 3.11. Your code never ran, and it cost you no GPU
  time.
- **run is red** → your code. The step prints your own output, so the
  traceback is right there.
- **both green** → the summary at the top of the run page says how long you
  queued, how long you ran, how much of your 40 GPU-hours that leaves, and
  which files your job wrote.

If the **run** step says it stopped watching, nothing was cancelled — GitHub
runners do not wait forever. `habs status` picks the job back up.

## Reading what your job produced

Your results are in your own storage. Two ways to get at them, and the first
one is the one you want.

**Open them in a file browser.** Install
[Azure Storage Explorer](https://azure.microsoft.com/products/storage/storage-explorer)
— free, Mac/Windows/Linux. Then:

1. Click the plug icon (*Connect to a resource*)
2. **Blob container** → **Shared access signature URL (SAS)**
3. Paste the **results link** HABS sent you → *Next* → *Connect*

Your container appears in the sidebar. Open `out/` and every job you have run
is a folder in there; double-click a file to look at it, or right-click to
download. `logs/` holds the full output of every job.

**Or from a terminal**, if you prefer:

```bash
export HABS_SAS='<the results link>'

habs status          # your jobs, and why any of them is waiting
habs watch           # follow your latest job to the end
habs ls              # what your latest job wrote
habs get             # download it
habs logs            # the whole log
```

Nobody else can read your container, and you cannot read anyone else's.

## Running on your own machine first

```bash
pip install -r requirements.txt
pip install "habs-hack[storage] @ https://github.com/HABS-BRAIN/habs-hack/releases/download/v0.3.0/habs_hack-0.3.0-py3-none-any.whl"

habs run --data ./sample --out ./out
```

`sample/` is six short recordings committed in this repo, in the same layout as
the real dataset. It is enough to prove your code runs before it queues.

The client is installed separately on purpose. `requirements.txt` is what goes
into the container your job runs in, and the client has no business being in
there — the platform runs your code itself.

Same contract, your laptop, no queue. Worth doing before every push — a job
that fails in the first ten seconds has still cost your team its turn.

## Limits

| | |
| --- | --- |
| Jobs running at once, per team | 1 |
| Jobs you can have queued | 10 |
| Longest a single job may run | 1 hour, then it is stopped |

Teams are ordered by how much compute they have already used, so a team that
submits ten jobs does not push anyone else back ten places.

## When it goes wrong

The Actions run is the whole story. Which of the two steps is red already
tells you whether to look at `requirements.txt` or at `process.py`, and the
log of that step says the rest — including, if the platform broke rather than
your code, a line saying so. Bring the link to a mentor and it is usually
enough.
