import os
from openai import OpenAI

class OpenAIGateway:
    """
    Capa de infraestructura: maneja la conexión directa con la API de OpenAI.
    La capa de aplicación (openai_service) solo la utiliza como intermediario.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable de entorno OPENAI_API_KEY en el archivo .env.")
        self.client = OpenAI(api_key=api_key)

    def generar_respuesta(self, prompt: str) -> str:
        """
        Envía un prompt a OpenAI y devuelve el texto generado.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # puedes usar gpt-3.5-turbo si prefieres
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=350
        )
        return response.choices[0].message.content
