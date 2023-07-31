import os
import re
from fastapi import APIRouter
from smb.SMBConnection import SMBConnection
from dotenv import load_dotenv
from trakt import Trakt

load_dotenv()

router = APIRouter()

Trakt.configuration.defaults.client(
    id=os.getenv('TRAKT_CLIENT_ID'),
    secret=os.getenv('TRAKT_CLIENT_SECRET')
)

@router.get("/list_files")
def list_files():
    try:
        # Configura la conexión con el servidor Samba
        server = os.getenv('SAMBA_SERVER')
        username = ''
        password = ''
        share = 'media'
        directorio = 'pelis'

        conn = SMBConnection(username, password, 'python', 'samba')
        conn.connect(server)
        results = conn.listPath(share, directorio)
        patron = r'(.+)\s\((\d{4})\)'

        for obj in results:
            print(obj.filename)
            if obj.filename not in [".", ".."]:
                coincidencia = re.match(patron, obj.filename)
                if coincidencia:
                    # Extraer el nombre y el año de las coincidencias
                    peli = coincidencia.group(1)
                    anio = coincidencia.group(2)
                    trakt_return = Trakt['search'].query(
                        media = 'movie',
                        query = peli,
                        year = anio,
                        extended = 'full'
                    )
                    print(trakt_return)


        return [obj.filename for obj in results if obj.filename not in [".", ".."]]

    except Exception as e:
        return {"error": str(e)}
