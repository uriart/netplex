from fastapi import APIRouter
from smb.SMBConnection import SMBConnection

router = APIRouter()

server = '192.168.0.16'
username = ''
password = ''
share = 'media'
directorio = 'pelis'

@router.get("/list_files")
def list_files():
    try:
        conn = SMBConnection(username, password, 'python', 'samba')
        conn.connect(server)
        results = conn.listPath(share, directorio)
        return [obj.filename for obj in results if obj.filename not in [".", ".."]]
    except Exception as e:
        return {"error": str(e)}
    
@router.delete("/delete_directory/{path}")
def delete_directory(path):
    try:
        conn = SMBConnection(username, password, 'python', 'samba')
        conn.connect(server)
        delete_directory_recursive(conn, share, directorio + "/" + path)

        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def delete_directory_recursive(conn, share_name, directory_path):
    # Obtener la lista de archivos y subdirectorios dentro del directorio
    files = conn.listPath(share_name, directory_path)
    # Eliminar archivos dentro del directorio
    for f in files:
        if f.filename not in ['.', '..']:
            print(f.filename)
            file_path = share_name + '/' + directory_path + '/' + f.filename
            if f.isDirectory:
                # Si es un subdirectorio, eliminar recursivamente
                delete_directory_recursive(conn, file_path)
            else:
                # Si es un archivo, eliminarlo
                try:
                    conn.deleteFiles(share_name, file_path)
                except Exception as e:
                    print(e)
                    return {"error": str(e)}
    
    # Eliminar el directorio en sí
    conn.deleteDirectory(share_name, directory_path)