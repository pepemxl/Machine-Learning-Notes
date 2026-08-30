# Sistemas de Detección

Por dentro, este sistema de detección es un sistema **NLU multifuncional** —similar a spaCy—
pero basado en una arquitectura monolítica y enfocado en **contenido generado por usuarios**.

Todas las funciones se exponen usando los mismos modelos de lenguaje y el mismo proceso de
análisis, invocado mediante el método `POST /parse`. En una sola llamada obtienes entidades,
sentimiento, tema, contenido problemático y datos de NLP de bajo nivel.

## Extracción de entidades

Estos son los tipos de entidades que se extraen:

- **persona**, con subtipos opcionales:
    - `fictional_character` — personajes de libros, películas, etc.
    - `important_person` — VIPs, celebridades, figuras históricas, políticos, etc.
    - `spiritual_being` — dioses, espíritus, etc.
- **organización**
- **lugar**
- **rango de tiempo**
- **fecha**
- **hora**
- **cantidad de dinero**
- **número de teléfono**
- **rol** — rol social (profesión, rango, etc.)
- **direcciones de criptomonedas**, con subtipos opcionales: bitcoin, ethereum, monero,
  monero_payment_id, litecoin, dash
- **números de tarjeta de crédito**, con subtipos: visa, mastercard, american express,
  diners club, discovery, jcb, unionpay
- **sitio web**
- **software**
- **nombre de archivo**
- **dirección IP**, con subtipos:
    - v4
    - v6 (en desarrollo)
- **dirección MAC**
- **nombre de usuario**

## Identificación del idioma

Detecta el idioma del enunciado.

## Análisis de sentimiento

Análisis de sentimiento tanto **a nivel de documento** como desglosado **por aspectos o
facetas** (lo que se conoce como *aspect-based sentiment analysis*).

Conviene señalar que el análisis de sentimiento y la detección de contenido problemático **no
son lo mismo**. El sentimiento puede ser negativo sin constituir un ataque personal o discurso
de odio; y a la inversa, la actividad delictiva o las insinuaciones sexuales no necesariamente
llevan un sentimiento negativo asociado.

## Ver también

- [Detección de patrones de nombres](deteccion_de_patrones_de_nombres.md)
