
import sys
from pathlib import Path

def file_to_md(input_file, output_md=None):
    """
    将单个代码文件转换为 Markdown 文件，自动识别语言并插入代码块。
    不处理文件夹，仅转换指定文件。
    """
    file_path = Path(input_file)
    if not file_path.exists():
        print(f"❌ 文件不存在: {input_file}")
        return

    # 支持的语言映射
    lang_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.sh': 'bash',
        '.md': 'markdown',
        '.yml': 'yaml'
    }

    lang = lang_map.get(file_path.suffix.lower(), '')
    content = file_path.read_text(encoding='utf-8')

    # 输出文件名默认为源文件名 + .md
    if output_md is None:
        output_md = file_path.with_suffix('.md')

    with open(output_md, 'w', encoding='utf-8') as md:
        md.write(f"# `{file_path.name}` 代码片段\n\n")
        md.write(f"```{lang}\n")
        md.write(content)
        md.write("\n```\n")
    
    print(f"✅ 已生成: {output_md}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_to_md.py <path/to/your/file.py>")
        sys.exit(1)
    print(sys.argv)
    file_to_md(sys.argv[1])
