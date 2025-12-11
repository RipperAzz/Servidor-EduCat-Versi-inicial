# Servidor-EduCat-Versio-inicial
La vesió inicial del servidor EduCat pel projecte de Treball De Recerca.

Servidor backend per a l’aplicació educativa EduCat, desenvolupat com a part del Treball de Recerca (TDR).
Implementat amb FastAPI, SQLAlchemy, Pydantic i SQLite.

Tecnologies principals:
- Python 3.10+
- FastAPI (Framework Principal)
- Uvicorn (servidor ASGI)
- SQLAlchemy (ORM per a la BD)
- Pydantic (validació de dades)
- SQLite (base de dades local)
- JWT (autenticació)

Configuració de l'aplicaió
-> Crea un fitxer .env a l'arrel del projecte
Exemple:
 SECRET_KEY="your-secret-key"
 ALGORITHM="HS256"
 DATABASE_URL="sqlite:///./mi_base.db"

Executa "pip install -r requirements.txt" Dins del projecte

Per la seva utilitzció es possible que s'hagin de modificar diferents camps en el codi dels arxius!
