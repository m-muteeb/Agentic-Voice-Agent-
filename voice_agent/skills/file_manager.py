import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def create_file(path, content=""):
    """
    Creates a new file with optional content.
    Returns success message or error.
    """
    try:
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File created successfully at {path}"
    except Exception as e:
        return f"Error creating file: {e}"

def create_folder(path):
    """
    Creates a new folder/directory.
    Returns success message or error.
    """
    try:
        path = os.path.expanduser(path)
        os.makedirs(path, exist_ok=True)
        return f"Folder created successfully at {path}"
    except Exception as e:
        return f"Error creating folder: {e}"

def delete_item(path):
    """
    Deletes a file or folder.
    Returns success message or error.
    """
    try:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Item not found: {path}"
        
        if os.path.isfile(path):
            os.remove(path)
            return f"File deleted: {path}"
        else:
            shutil.rmtree(path)
            return f"Folder deleted: {path}"
    except Exception as e:
        return f"Error deleting item: {e}"

def rename_item(old_path, new_path):
    """
    Renames or moves a file or folder.
    Returns success message or error.
    """
    try:
        old_path = os.path.expanduser(old_path)
        new_path = os.path.expanduser(new_path)
        
        if not os.path.exists(old_path):
            return f"Item not found: {old_path}"
        
        os.rename(old_path, new_path)
        return f"Item renamed/moved from {old_path} to {new_path}"
    except Exception as e:
        return f"Error renaming item: {e}"

def copy_item(source, destination):
    """
    Copies a file or folder to a new location.
    Returns success message or error.
    """
    try:
        source = os.path.expanduser(source)
        destination = os.path.expanduser(destination)
        
        if not os.path.exists(source):
            return f"Source not found: {source}"
        
        if os.path.isfile(source):
            shutil.copy2(source, destination)
            return f"File copied from {source} to {destination}"
        else:
            shutil.copytree(source, destination)
            return f"Folder copied from {source} to {destination}"
    except Exception as e:
        return f"Error copying item: {e}"

def search_files(query, location=None, extension=None, max_results=20):
    """
    Searches for files matching the query.
    Returns list of matching file paths.
    """
    try:
        if location is None:
            # Default search locations
            search_paths = [
                os.path.expanduser("~/Documents"),
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/Downloads")
            ]
        else:
            location = os.path.expanduser(location)
            search_paths = [location]
        
        results = []
        query_lower = query.lower()
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            for root, dirs, files in os.walk(search_path):
                # Limit depth to avoid excessive searching
                if root.count(os.sep) - search_path.count(os.sep) > 3:
                    continue
                
                for file in files:
                    # Check extension filter
                    if extension and not file.endswith(extension):
                        continue
                    
                    # Check name match
                    if query_lower in file.lower():
                        full_path = os.path.join(root, file)
                        results.append(full_path)
                        
                        if len(results) >= max_results:
                            break
                
                if len(results) >= max_results:
                    break
        
        if results:
            return f"Found {len(results)} file(s):\n" + "\n".join(results[:10])
        else:
            return f"No files found matching '{query}'"
            
    except Exception as e:
        return f"Error searching files: {e}"

def get_file_info(path):
    """
    Gets detailed information about a file or folder.
    Returns formatted info string.
    """
    try:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Item not found: {path}"
        
        stat_info = os.stat(path)
        size_bytes = stat_info.st_size
        
        # Convert size to human readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                size_str = f"{size_bytes:.2f} {unit}"
                break
            size_bytes /= 1024.0
        
        modified_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        item_type = "Folder" if os.path.isdir(path) else "File"
        
        info = f"{item_type}: {os.path.basename(path)}\n"
        info += f"Size: {size_str}\n"
        info += f"Modified: {modified_time}\n"
        info += f"Location: {os.path.dirname(path)}"
        
        return info
    except Exception as e:
        return f"Error getting file info: {e}"

def open_location(path):
    """
    Opens the file or folder location in Windows Explorer.
    Returns success message or error.
    """
    try:
        path = os.path.expanduser(path)
        
        if not os.path.exists(path):
            return f"Location not found: {path}"
        
        # If it's a file, open the containing folder
        if os.path.isfile(path):
            folder = os.path.dirname(path)
            os.startfile(folder)
            return f"Opened folder containing {os.path.basename(path)}"
        else:
            os.startfile(path)
            return f"Opened folder: {path}"
    except Exception as e:
        return f"Error opening location: {e}"

def list_directory(path="."):
    """
    Lists contents of a directory.
    Returns formatted list of files and folders.
    """
    try:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Directory not found: {path}"
        
        if not os.path.isdir(path):
            return f"Not a directory: {path}"
        
        items = os.listdir(path)
        if not items:
            return f"Directory is empty: {path}"
        
        folders = [f"📁 {item}" for item in items if os.path.isdir(os.path.join(path, item))]
        files = [f"📄 {item}" for item in items if os.path.isfile(os.path.join(path, item))]
        
        result = f"Contents of {path}:\n"
        result += "\n".join(folders + files)
        
        return result
    except Exception as e:
        return f"Error listing directory: {e}"
