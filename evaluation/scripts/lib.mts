import fs from "node:fs";
import path from "node:path";
const ROOT = path.resolve(import.meta.dirname, "..");
export function datasetRoot(_name: string): string { return path.join(ROOT, "data"); }
export function gradingRoot(): string { return path.join(ROOT, "grading"); }
export function datasetCases(name: string, split: string): any[] {
  if (!["optimization", "test"].includes(split)) throw new Error("split 必须为 optimization 或 test");
  return JSON.parse(fs.readFileSync(path.join(datasetRoot(name), "split-manifest.json"), "utf8")).cases
    .filter((item: any) => item.split === split).sort((a: any, b: any) => a.case_id.localeCompare(b.case_id));
}
export function parseArgs(argv: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i]; const value = argv[i + 1];
    if (!key?.startsWith("--") || !value || value.startsWith("--")) throw new Error("参数需使用 --名称 值");
    if (!["split", "version", "experiment"].includes(key.slice(2))) throw new Error(`未知参数：${key}`);
    out[key.slice(2)] = value;
  }
  return out;
}
export function required(args: Record<string,string>, key: string): string {
  if (!args[key]?.trim()) throw new Error(`缺少参数 --${key}`);
  return args[key];
}
export function writeJson(file: string, value: unknown): void {
  fs.mkdirSync(path.dirname(file), {recursive:true});
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + "\n");
}
