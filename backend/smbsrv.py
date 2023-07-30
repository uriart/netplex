from fastapi import APIRouter
from smb.SMBConnection import SMBConnection
import json

router = APIRouter()

@router.get("/list_files")
def list_files():
    try:
        # Configura la conexión con el servidor Samba
        server = '192.168.0.16'
        username = ''
        password = ''
        share = 'media'
        directorio = 'pelis'

        conn = SMBConnection(username, password, 'python', 'samba')
        conn.connect(server)
        results = conn.listPath(share, directorio)

        data = {
            "movies": [obj.filename for obj in results if obj.filename not in [".", ".."]]
        }

        return [obj.filename for obj in results if obj.filename not in [".", ".."]]

    except Exception as e:
        return {"error": str(e)}
