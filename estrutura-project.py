import os

def list_files(startpath):
    with open('file_structure.txt', 'w') as f:
        for root, dirs, files in os.walk(startpath):
            # Ignorar o diretório .git
            dirs[:] = [d for d in dirs if d != '.git']
            
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for i, file in enumerate(files):
                if i == len(files) - 1:
                    f.write('{}└── {}\n'.format(subindent, file))
                else:
                    f.write('{}├── {}\n'.format(subindent, file))

if __name__ == "__main__":
    startpath = '.'  # Caminho inicial (diretório atual)
    list_files(startpath)