def upgrade_headings(md_content):
    lines = md_content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('##'):
            lines[i] = line[1:]
    return '\n'.join(lines)

def main():
    source = input('源文件:')
    result = input('结果文件:')
    with open(source, 'r') as f:
        md_content = f.read()
    
    new_md_content = upgrade_headings(md_content)
    
    with open(result, 'w') as f:
        f.write(new_md_content)

if __name__ == "__main__":
    main()
