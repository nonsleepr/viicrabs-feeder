import httpx
import keyring
from rich import print

ACCOUNT_KEY = "AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys"

class SevenCrabsFeeder:
    def __init__(self, email = None, password = None):
        if email and password:
            if creds := keyring.get_credential("xilabs-reader", None):
                keyring.delete_password("xilabs-reader", creds.username)
            keyring.set_password("xilabs-reader", email, password)
        else:
            creds = keyring.get_credential("xilabs-reader", None)
            if not creds:
                raise Exception("No credentials found")
            email = creds.username
            password = creds.password
        self.email = email
        self.password = password
        self.token = None

    async def login(self) -> dict:
        """
        Login to ElevenLabs using email and password.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={ACCOUNT_KEY}",
                json={
                    "returnSecureToken": True,
                    "email": self.email,
                    "password": self.password,
                    "clientType": "CLIENT_TYPE_WEB",
                },
                headers={
                    "Origin": "https://elevenlabs.io",
                },
            )
            """
            Response contains:
                - kind
                - localId
                - email
                - displayName
                - idToken
                - registered
                - profilePicture
                - refreshToken
                - expiresIn
            """
            response.raise_for_status()
            self.token = response.json()["idToken"]

    async def add_article(self, content = None, **kwargs) -> dict:
        """
        Add text to ElevenLabs Reader.
        """
        if not self.token:
            await self.login()
        files = {
            "from_document": (kwargs.pop('file_name', 'source.txt'),
                              content,
                              kwargs.pop('file_type', 'text/plain'),
                             ),
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.elevenlabs.io/v1/reader/reads/add",
                data=kwargs,
                files=files,
                headers={
                    "Authorization": f"Bearer {self.token}",
                },
            )
            response.raise_for_status()
            return response.json()

    async def add_podcast(self, content = None, **kwargs) -> dict:
        """
        Request GenFM podcast creation.
        """
        if not self.token:
            await self.login()
        files = {
            "from_document": (kwargs.pop('file_name', 'source.txt'),
                              content,
                              kwargs.pop('file_type', 'text/plain'),
                             ),
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.elevenlabs.io/v1/reader/reads/add",
                data=kwargs,
                files=files,
                headers={
                    "Authorization": f"Bearer {self.token}",
                },
            )
            return response.json()

    async def delete_article(self, read_id: str) -> dict:
        """
        Add text to ElevenLabs Reader.
        """
        if not self.token:
            await self.login()
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"https://api.elevenlabs.io/v1/reader/reads/{read_id}",
                headers={
                    "Authorization": f"Bearer {self.token}",
                },
            )
            response.raise_for_status()
            return response.json()
