import httpx

async def login(email, password) -> dict:
    """
    Login to ElevenLabs using email and password.

    Returns a dictionary with the following keys:
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
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys",
            json={
                "returnSecureToken": True,
                "email": email,
                "password": password,
                "clientType": "CLIENT_TYPE_WEB",
            },
            headers={
                "Origin": "https://elevenlabs.io",
            },
        )
        return response.json()

async def add_article(text='', token=None, **kwargs) -> dict:
    """
    Add text to ElevenLabs Reader.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.elevenlabs.io/v1/reader/reads/add",
            data=kwargs,
            files={"from_document": ('source.txt', text, 'text/plain')},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        return response.json()

async def add_podcast(text='', token=None, **kwargs) -> dict:
    """
    Request GenFM podcast creation.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.elevenlabs.io/v1/reader/reads/add_podcast",
            data=kwargs,
            files={"from_document": ('source.txt', text, 'text/plain')},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        return response.json()