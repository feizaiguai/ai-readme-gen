#!/usr/bin/env python3
"""
AI Readme Generator - 智能 README 生成器
自动分析项目结构生成专业的 README 文档
"""

import os
import ast
from typing import List, Dict, Any
from colorama import init, Fore, Style

init(autoreset=True)


class ReadmeGenerator:
    """README 生成器"""
    
    def __init__(self):
        self.project_name = ""
        self.language = "python"  # 默认 Python 项目
        self.structure = {}
        self.dependencies = []
        self.main_modules = []
    
    def generate(self, project_path: str) -> str:
        """生成 README"""
        if not os.path.exists(project_path):
            print(f"{Fore.RED}错误: 路径不存在 - {project_path}")
            return ""
        
        self.project_name = os.path.basename(project_path)
        
        print(f"{Fore.CYAN}正在分析项目: {project_path}\n")
        
        # 分析项目结构
        self._analyze_structure(project_path)
        
        # 检测语言
        self._detect_language()
        
        # 生成 README
        readme = self._build_readme()
        
        return readme
    
    def _analyze_structure(self, path: str):
        """分析项目结构"""
        self.structure = {
            'directories': [],
            'files': [],
            'code_files': []
        }
        
        for root, dirs, files in os.walk(path):
            # 跳过隐藏文件和目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv']]
            
            rel_root = os.path.relpath(root, path)
            if rel_root == '.':
                rel_root = ''
            
            for dir_name in dirs:
                dir_path = os.path.join(rel_root, dir_name) if rel_root else dir_name
                self.structure['directories'].append(dir_path)
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(rel_root, file) if rel_root else file
                self.structure['files'].append(file_path)
                
                # 统计代码文件
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs')):
                    self.structure['code_files'].append(file_path)
    
    def _detect_language(self):
        """检测编程语言"""
        files = self.structure['files']
        
        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
        }
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in extensions:
                self.language = extensions[ext].lower()
                break
    
    def _build_readme(self) -> str:
        """构建 README"""
        lines = []
        
        # 标题
        lines.append(f"# {self.project_name}\n")
        lines.append("\n> 🔥 智能生成的 README 文档\n")
        
        # 项目简介
        lines.append("## 📖 项目简介\n")
        lines.append(f"这是一个使用 **{self.language.title()}** 开发的项目。\n")
        lines.append(f"项目包含 {len(self.structure['directories'])} 个目录和 {len(self.structure['files'])} 个文件。\n")
        
        # 目录结构
        lines.append("\n## 📁 项目结构\n")
        lines.append("```\n")
        lines.append(self.project_name + "/\n")
        
        for dir_name in sorted(self.structure['directories'])[:5]:  # 最多显示5层
            lines.append(f"├── {dir_name}/\n")
        
        # 显示部分文件
        for file in sorted(self.structure['files'])[:10]:
            lines.append(f"├── {file}\n")
        
        lines.append("```\n")
        
        # 安装指南
        lines.append("\n## 🚀 安装指南\n")
        
        if 'package.json' in self.structure['files']:
            lines.append("```bash\nnpm install\n```\n")
        elif 'requirements.txt' in self.structure['files']:
            lines.append("```bash\npip install -r requirements.txt\n```\n")
        elif 'go.mod' in self.structure['files']:
            lines.append("```bash\ngo mod download\n```\n")
        else:
            lines.append("```bash\n# 安装依赖\n```\n")
        
        # 使用方法
        lines.append("\n## 💡 使用方法\n")
        
        if self.language == 'python':
            main_file = [f for f in self.structure['code_files'] if 'main' in f.lower() or f == 'app.py']
            if main_file:
                lines.append(f"```bash\npython {main_file[0]}\n```\n")
        elif self.language in ['javascript', 'typescript']:
            lines.append("```bash\nnpm start\n```\n")
        
        # 贡献指南
        lines.append("\n## 🤝 贡献指南\n")
        lines.append("1. Fork 本仓库\n")
        lines.append("2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)\n")
        lines.append("3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)\n")
        lines.append("4. 推送到分支 (`git push origin feature/AmazingFeature`)\n")
        lines.append("5. 创建 Pull Request\n")
        
        # 许可证
        lines.append("\n## 📄 许可证\n")
        lines.append("本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件\n")
        
        # 联系方式
        lines.append("\n## 📧 联系方式\n")
        lines.append("邮箱: 196408245@qq.com\n")
        
        return ''.join(lines)


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}使用方法: python main.py <项目目录>")
        print(f"示例: python main.py ./my-project")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    generator = ReadmeGenerator()
    readme = generator.generate(project_path)
    
    if readme:
        # 保存 README.md
        output_path = os.path.join(project_path, 'README.md')
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(readme)
            print(f"\n{Fore.GREEN}✓ README.md 已生成: {output_path}")
        except Exception as e:
            print(f"\n{Fore.GREEN}生成的 README:\n")
            print(readme)
            print(f"\n{Fore.RED}保存失败: {str(e)}")


if __name__ == '__main__':
    main()
