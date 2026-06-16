# OpenCode Course Setup

This folder contains OpenCode setup notes for the course. Start by connecting
OpenAI inside OpenCode, then optionally add the e-INFRA CZ provider and Chimera
MCP servers used in the workshop.

It also contains [`ChimeraResearchTeam/`](ChimeraResearchTeam/), a copy-pasteable
OpenCode team of research agents, subagents, commands, skills, and templates.
If you want to use that team with the Chimera MCP tools, set up the e-INFRA
provider config below first, then follow
[`ChimeraResearchTeam/README.md`](ChimeraResearchTeam/README.md) to install the
team into a project.

The example [`opencode.json`](opencode.json) is safe to share because it does not
contain an API token. It reads the e-INFRA token from the environment variable
`E_INFRA_API_TOKEN`.

## 1. Connect OpenAI in OpenCode

> **_NOTE:_**  If you are attending the RSE course, you should be given an OpenAI API key for
the course. If you do not receive one, ask the course team for it.

Start OpenCode from the project you want to work in:

```bash
cd /path/to/your/project
opencode
```

Inside OpenCode, run:

```text
/connect
```

Choose the OpenAI provider. If OpenCode asks for the auth method, choose the
manual API key option, paste the course OpenAI API key, and confirm. Treat the
key like a password: do not paste it into `opencode.json`, commit it to Git, or
share it in screenshots.

After connecting, choose a model:

```text
/models
```

Select the OpenAI model recommended by the course team.

If the course team asks you to use the OpenCode-hosted provider instead, use
the same `/connect` command, choose `OpenCode Zen`, follow the browser sign-in
flow, and paste the key or token when OpenCode asks for it.

## 2. Add e-INFRA for course infrastructure

The e-INFRA setup is needed if you want to use the shared e-INFRA models or the
Chimera MCP tools from the example config.

### 2.1 Get an e-INFRA API token

1. Open [https://chat.ai.e-infra.cz](https://chat.ai.e-infra.cz).
2. Sign in with your institutional or e-INFRA identity.
3. Find the account/settings area for API keys or API tokens.
4. Create or copy an API token.

If the API token section is not visible, ask your instructor, project PI, or
local e-INFRA administrator to confirm that your account has access to the
e-INFRA AI/LLM service.

Treat the token like a password. Do not paste it into `opencode.json`, do not
commit it to Git, and do not share it in screenshots.

### 2.2 Save the e-INFRA token for OpenCode

OpenCode reads the token from `E_INFRA_API_TOKEN`, because
[`opencode.json`](opencode.json) contains:

```json
"apiKey": "{env:E_INFRA_API_TOKEN}"
```

For the current terminal session:

```bash
export E_INFRA_API_TOKEN="paste-your-token-here"
```

To make it persistent on macOS or Linux, add the same line to your shell profile.
For example, for the default macOS `zsh` shell:

```bash
nano ~/.zshrc
# If your terminal uses bash instead, use:
# nano ~/.bashrc
```

Add:

```bash
export E_INFRA_API_TOKEN="paste-your-token-here"
```

Then reload the shell:

```bash
source ~/.zshrc
# If you added the line to ~/.bashrc instead, use:
# source ~/.bashrc
```

On Windows PowerShell, set it for your user account:

```powershell
[Environment]::SetEnvironmentVariable("E_INFRA_API_TOKEN", "paste-your-token-here", "User")
```

Open a new terminal after setting the variable.

### 2.3 Copy the OpenCode config

OpenCode can load config from a global user location or from a project root.
Use one of these options.

### Option A: global config

Use this if you want the e-INFRA models available in every project.

From this repository root:

```bash
mkdir -p ~/.config/opencode
cp OpenCode/opencode.json ~/.config/opencode/opencode.json
```

### Option B: project config

Use this if you want the config only for one project.

Copy the file into the root of the project where you run OpenCode:

```bash
cp OpenCode/opencode.json /path/to/your/project/opencode.json
```

Then start OpenCode from that project directory:

```bash
cd /path/to/your/project
opencode
```

OpenCode also supports custom config paths with `OPENCODE_CONFIG`. See the
[OpenCode config documentation](https://opencode.ai/docs/config) for details.

### 2.4 Edit the Chimera MCP settings

The example config includes two MCP servers:

- `chimera-slurm`
- `chimera-filecompress`

Both use SSH and currently contain this placeholder:

```text
user@hpc.troja.mff.cuni.cz
```

Replace `user` with your Chimera/HPC login name before using the MCP tools.

You should also confirm that SSH works without an interactive password prompt,
because OpenCode starts the MCP servers in the background:

```bash
ssh user@hpc.troja.mff.cuni.cz
```

If you do not need the Chimera MCP tools, either remove the `mcp` section or set
the two servers to:

```json
"enabled": false
```

### 2.5 Choose an e-INFRA model

Run OpenCode from the project where the config applies:

```bash
opencode
```

Inside OpenCode:

```text
/models
```

Choose one of the e-INFRA models, for example:

- `einfra/kimi-k2.6`
- `einfra/coder`
- `einfra/agentic`
- `einfra/mini`
- `einfra/thinker`

The default model in this config is:

```json
"model": "einfra/kimi-k2.6"
```

You can change that value in `opencode.json` if the workshop or your project
uses a different model.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| OpenAI connection fails | Run `/connect` again inside OpenCode and confirm that you pasted the course OpenAI API key into the OpenAI provider flow. |
| OpenCode cannot see `einfra` models | Make sure `opencode.json` is in `~/.config/opencode/opencode.json` or in the project root where you run `opencode`. |
| Authentication fails | Check that `E_INFRA_API_TOKEN` is set in the same terminal where you start OpenCode. |
| MCP servers fail to start | Replace `user@hpc.troja.mff.cuni.cz` with your real HPC login and verify SSH access first. |
| A model is unavailable | Try an alias such as `einfra/coder`, `einfra/agentic`, `einfra/mini`, or `einfra/thinker`; these aliases can track current e-INFRA models. |
