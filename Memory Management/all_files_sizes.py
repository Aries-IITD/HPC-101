import os
import argparse

def get_size(start_path):
    total_size = 0
    if os.path.isfile(start_path):
        total_size = os.path.getsize(start_path)
    else:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size

def list_files_and_folders(directory):
    file_sizes = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            size = get_size(folder_path)
            file_sizes.append((folder_path, size))

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            size = get_size(file_path)
            file_sizes.append((file_path, size))
    return sorted(file_sizes, key=lambda x: x[1], reverse=True)

def main():
    parser = argparse.ArgumentParser(description="Calculate and sort sizes of files and folders")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("-n", type=int, help="Show top n largest files", default=None)

    args = parser.parse_args()
    files_and_folders = list_files_and_folders(args.directory)

    if args.n:
        files_and_folders = files_and_folders[:args.n]

    for path, size in files_and_folders:
        print(f"{path}: {size/1024/1024:.2f} MB")

if __name__ == "__main__":
    main()
