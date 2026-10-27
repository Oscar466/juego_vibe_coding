# 🎮 Juego en Pygame & Harness de Agentes Autónomos

> Un entorno de desarrollo estructurado para la creación y orquestación de videojuegos mediante flujos de trabajo colaborativos con agentes de IA.

---

## 🚀 ¿De qué trata este proyecto?
Este repositorio implementa un **harness de agentes autónomos** diseñado para orquestar el desarrollo de un juego en `Pygame`. Utilizando una división clara de roles, el sistema automatiza la planificación, implementación, pruebas y control de calidad de cada *sprint*.

---

## 📂 Arquitectura del Harness
La estructura del proyecto está diseñada bajo principios de separación de responsabilidades y trazabilidad estricta:

```text
juego_harness/
├── .opencode/
│   └── agents/           # Definición de roles y comportamientos de los agentes
│       ├── implementador.md
│       ├── leader.md
│       └── QA.md
├── .venv/                # Entorno virtual de Python
├── aprobado/             # Historial de cierres de sprint y tareas validadas
├── assets/               # Recursos gráficos y multimedia del juego
├── specs/                # Especificaciones técnicas y requisitos globales
├── src/                  # Código fuente principal (Pygame)
├── tasks/                # Tareas modulares asignadas por rol
├── .gitignore
├── AGENTS.md             # Reglas globales de orquestación
└── requirements.txt      # Dependencias del proyecto
