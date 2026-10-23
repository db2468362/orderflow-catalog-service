import { tool, type Plugin } from "@opencode-ai/plugin";

export const PysCodeStylePlugin: Plugin = async ({ $, directory, worktree }) => {
  const projectRoot = worktree || directory;

  const runPys = async (mode: "format" | "check") => {
    const result = await $`uv run pys ${mode} .`
      .cwd(projectRoot)
      .nothrow();
    const stdout = result.stdout.toString().trim();
    const stderr = result.stderr.toString().trim();
    const output = [stdout, stderr].filter(Boolean).join("\n");

    return [
      `Command: pys ${mode} . (via uv run)`,
      `Exit code: ${result.exitCode}`,
      output || "No output.",
    ].join("\n");
  };

  return {
    tool: {
      pys_format: tool({
        description:
          "Format the project with `pys format .`. This command may modify files.",
        args: {},
        execute: async () => runPys("format"),
      }),
      pys_check: tool({
        description: "Check the project code style with `pys check .`.",
        args: {},
        execute: async () => runPys("check"),
      }),
    },
  };
};
