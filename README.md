# Guild Wars 1 — Daily Activities Discord Bot

A lightweight Discord bot that automatically publishes the daily activities of **Guild Wars 1** to a Discord channel.

The bot is designed to run as a scheduled **GitHub Actions** workflow, so no server or always-on machine is required.

The current version supports:

- Zaishen Bounty
- Zaishen Combat
- Zaishen Mission
- Zaishen Vanquish
- Ascalonian Vanguard
- Shining Blade
- Nicholas Sandford

The activities are calculated from local rotation data, so the bot does not need to query the Guild Wars Wiki every day.

---

# 🇬🇧 English

## How it works

The project uses **GitHub Actions** as a cron scheduler. The bot runs automatically every day at 16:05 UTC using GitHub Actions. If you want to test the bot manually, you can also run the workflow directly from the Actions section of your GitHub repository, without having to wait for the scheduled execution.

At the configured time, GitHub Actions:

1. Starts a Python environment.
2. Loads the activity rotation data.
3. Calculates the activities for the current day.
4. Builds a Discord embed.
5. Sends the embed to the configured Discord channel.

The project therefore does not require a permanent server.

### Architecture

```text
GitHub Actions
      │
      │ scheduled execution
      ▼
   main.py
      │
      ▼
DailyActivitiesEmbed
      │
      ├── Zaishen rotations
      ├── Vanguard rotation
      ├── Shining Blade rotation
      └── Nicholas Sandford rotation
      │
      ▼
Discord Embed
      │
      ▼
Discord Channel
```

---

# Getting Started

## 1. Fork the repository

First, create your own **fork** of this repository on GitHub.

The bot is intended to run from your own repository because the Discord webhook
URL must be stored as a repository secret.

---

## 2. Create a Discord webhook

Create a webhook in the Discord channel where you want the bot to publish the
daily activities.

In Discord:

1. Open your server.
2. Go to the channel where the daily activities should be posted.
3. Open the channel settings.
4. Go to **Integrations**.
5. Open **Webhooks**.
6. Create a new webhook.
7. Give it a suitable name, for example:
   `GW1 Daily Activities`.
8. Make sure the webhook belongs to the channel where you want the messages
   to appear.
9. Copy the webhook URL.

Keep the webhook URL private. Anyone who has it may be able to post messages
to the configured channel.

---

## 3. Create the GitHub repository secret

In your forked repository, go to:

```text
Settings
    → Secrets and variables
        → Actions
            → New repository secret
```

Create a secret named exactly:

```text
DISCORD_WEBHOOK_URL
```

The name is case-sensitive.

---

## 4. Add the Discord webhook URL

Paste the Discord webhook URL obtained in the previous step into the secret's
**Secret** field.

The final configuration should look conceptually like:

```text
Name:
DISCORD_WEBHOOK_URL

Secret:
https://discord.com/api/webhooks/...
```

Do **not** put the webhook URL directly in `config.yaml`, Python source files,
GitHub workflow files, or any other file committed to the repository.

The repository should only contain the secret name:

```text
DISCORD_WEBHOOK_URL
```

---

## 5. Configure the bot

The presentation of the Discord embed can be customized through:

```text
config.yaml
```

Example:

```yaml
discord:
  daily:
    title: "🎮 Guild Wars 1 — Daily Activities"
    description: "{date}"

    labels:
      "Zaishen Bounty": "🎯 Zaishen Bounty"
      "Zaishen Combat": "⚔️ Zaishen Combat"
      "Zaishen Mission": "📜 Zaishen Mission"
      "Zaishen Vanquish": "💀 Zaishen Vanquish"
      "Vanguard Quest": "🛡️ Vanguard"
      "Shining Blade": "⚔️ Shining Blade"
      "Nicholas Sandford": "🎒 Nicholas Sandford"
```

---

# Configuration

The goal is to keep presentation-related configuration outside the Python
code.

## Title

The `title` controls the title displayed at the top of the Discord embed.

For example:

```yaml
title: "🎮 Guild Wars 1 — Daily Activities"
```

can be changed to:

```yaml
title: "⚔️ Guild Wars 1 — Today's Activities"
```

---

## Description

The `description` controls the text displayed below the title.

The following variables are available:

| Variable | Description | Example |
|---|---|---|
| `{date}` | Current date | `15/08/2026` |
| `{date_iso}` | ISO formatted date | `2026-08-15` |

Example:

```yaml
description: "Daily Guild Wars 1 activities — {date}"
```

will produce:

```text
Daily Guild Wars 1 activities — 15/08/2026
```

---

## Activity names

The `labels` section allows you to customize the name displayed for each
activity.

For example:

```yaml
"Vanguard Quest": "🛡️ Vanguard"
```

can be changed to:

```yaml
"Vanguard Quest": "⚔️ Ascalonian Vanguard"
```

This only changes the presentation in Discord. It does not change the
underlying activity data.

---

# Activity data

Rotation data is stored locally under:

```text
data/source/
```

The project currently contains:

```text
zaishen_bounty.json
zaishen_combat.json
zaishen_missions.json
zaishen_vanquish.json
vanguard_quest.json
shining_blade.json
nicholas_sandford.json
```

The JSON files contain information such as:

- Reference date
- Reset time
- Cycle length
- Activity order
- Wiki URLs
- Locations
- Rewards
- Required items

This allows the bot to generate useful Discord links without querying the Wiki
during execution.

---

# Zaishen reward data

Zaishen activities use:

```text
data/source/zaishen_data.csv
```

This file contains the additional information required to enrich Zaishen
activities, including their Wiki URL and Zaishen Coin rewards.

The daily activity is first obtained from the rotation JSON and then matched
against this CSV.

```text
Zaishen rotation JSON
        │
        ▼
Activity of the day
        │
        ▼
zaishen_data.csv
        │
        ▼
Enriched information
        │
        ▼
Discord Embed
```

---

# Running locally

The bot can be executed manually with:

```bash
python src/main.py
```

This is useful for testing the generated Discord embed before relying on the
GitHub Actions workflow.

Make sure that `DISCORD_WEBHOOK_URL` is available in the environment when
running the bot locally.

---

# GitHub Actions

The production execution is handled by GitHub Actions.

The workflow acts as a cron job and executes the Python program automatically.

The Discord webhook URL is provided to the workflow through the repository
secret:

```text
DISCORD_WEBHOOK_URL
```

The webhook URL should never be committed to the repository.

---

# Project structure

A simplified version of the project looks like:

```text
gw_zaishen_activities_report/
│
├── .github/
│   └── workflows/
│       └── ...
│
├── data/
│   └── source/
│       ├── zaishen_data.csv
│       ├── zaishen_bounty.json
│       ├── zaishen_combat.json
│       ├── zaishen_missions.json
│       ├── zaishen_vanquish.json
│       ├── vanguard_quest.json
│       ├── shining_blade.json
│       └── nicholas_sandford.json
│
├── src/
│   ├── main.py
│   ├── daily_activities_embed.py
│   ├── zaishen_rotation.py
│   └── discord_client.py
│
├── config.yaml
└── README.md
```

---

# Roadmap

The current version focuses on daily Guild Wars 1 activities.

## Weekly activities

Add the weekly Guild Wars 1 activities using the same architecture as the
daily activities.

The intention is to keep the weekly logic independent from the daily embed
generation.

## Discord events

Create Discord scheduled events for relevant Guild Wars 1 activities.

This could make the bot useful not only for displaying information but also for
organizing group activities.

## Dungeon item prices

Add market price information for items that can be obtained from dungeons.

The objective is to eventually show information such as:

```text
Dungeon
 ├── Available items
 ├── Drop information
 └── Current market prices
```

This would make it possible to quickly identify which dungeons are currently
interesting from an economic perspective.

---

# 🇪🇸 Español

## ¿Qué es?

Este proyecto es un bot para **Discord** que publica automáticamente las
actividades diarias de **Guild Wars 1** en un canal de Discord.

El bot utiliza **GitHub Actions** como sistema de cron, por lo que no necesita
un servidor funcionando permanentemente. El bot se ejecuta automáticamente todos los días a las 16:05 UTC mediante GitHub Actions. Si quieres probar el bot manualmente, también puedes ejecutar el workflow directamente desde la sección Actions de tu repositorio de GitHub, sin tener que esperar a la ejecución programada.

Actualmente soporta:

- Zaishen Bounty
- Zaishen Combat
- Zaishen Mission
- Zaishen Vanquish
- Ascalonian Vanguard
- Shining Blade
- Nicholas Sandford

Las rotaciones se calculan utilizando datos almacenados localmente, por lo que
el bot no necesita consultar la Wiki de Guild Wars cada día.

---

# Primeros pasos

## 1. Haz un fork del repositorio

Primero debes crear un **fork** de este repositorio en tu propia cuenta de
GitHub.

El bot está pensado para ejecutarse desde tu propio repositorio, ya que la URL
del webhook de Discord debe almacenarse como un secret del repositorio.


---

## 2. Crea un webhook de Discord

Crea un webhook en el canal de Discord donde quieres que el bot publique las
diarias.

En Discord:

1. Abre tu servidor.
2. Ve al canal donde quieres recibir las actividades.
3. Abre la configuración del canal.
4. Entra en **Integraciones**.
5. Abre **Webhooks**.
6. Crea un nuevo webhook.
7. Dale un nombre, por ejemplo:
   `GW1 Daily Activities`.
8. Comprueba que el webhook pertenece al canal correcto.
9. Copia la URL del webhook.

Mantén la URL del webhook privada. Cualquier persona que la conozca podría
utilizarla para publicar mensajes en el canal asociado.

---

## 3. Crea el secret del repositorio

En tu fork, ve a:

```text
Settings
    → Secrets and variables
        → Actions
            → New repository secret
```

Crea un secret llamado exactamente:

```text
DISCORD_WEBHOOK_URL
```

El nombre distingue mayúsculas y minúsculas.

---

## 4. Añade la URL del webhook al secret

Pega la URL obtenida de Discord en el campo **Secret**.

La configuración debería ser conceptualmente:

```text
Name:
DISCORD_WEBHOOK_URL

Secret:
https://discord.com/api/webhooks/...
```

**No pongas la URL directamente en `config.yaml`, en el código Python, en el
workflow de GitHub ni en ningún otro fichero que vaya a subirse al
repositorio.**

El repositorio solo debe contener el nombre del secret:

```text
DISCORD_WEBHOOK_URL
```

---

## 5. Configura el bot

La presentación del embed de Discord se puede personalizar desde:

```text
config.yaml
```

Ejemplo:

```yaml
discord:
  daily:
    title: "🎮 Guild Wars 1 — Daily Activities"
    description: "{date}"

    labels:
      "Zaishen Bounty": "🎯 Zaishen Bounty"
      "Zaishen Combat": "⚔️ Zaishen Combat"
      "Zaishen Mission": "📜 Zaishen Mission"
      "Zaishen Vanquish": "💀 Zaishen Vanquish"
      "Vanguard Quest": "🛡️ Vanguard"
      "Shining Blade": "⚔️ Shining Blade"
      "Nicholas Sandford": "🎒 Nicholas Sandford"
```

---

# Configuración

La idea es mantener la configuración de presentación fuera del código Python.

## Título

`title` permite cambiar el título del embed.

```yaml
title: "🎮 Guild Wars 1 — Daily Activities"
```

Por ejemplo:

```yaml
title: "⚔️ Guild Wars 1 — Today's Activities"
```

---

## Descripción

`description` permite personalizar el texto que aparece debajo del título.

Variables disponibles:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `{date}` | Fecha actual | `15/08/2026` |
| `{date_iso}` | Fecha en formato ISO | `2026-08-15` |

Ejemplo:

```yaml
description: "Actividades diarias de Guild Wars 1 — {date}"
```

---

## Nombres de las actividades

La sección `labels` permite cambiar cómo se muestran las actividades.

Por ejemplo:

```yaml
"Vanguard Quest": "🛡️ Vanguard"
```

puede cambiarse por:

```yaml
"Vanguard Quest": "⚔️ Ascalonian Vanguard"
```

Esto únicamente modifica la presentación en Discord y no los datos internos de
la actividad.

---

# Datos de las actividades

Los datos de las rotaciones están almacenados en:

```text
data/source/
```

Actualmente se utilizan:

```text
zaishen_bounty.json
zaishen_combat.json
zaishen_missions.json
zaishen_vanquish.json
vanguard_quest.json
shining_blade.json
nicholas_sandford.json
```

Los JSON contienen información como:

- Fecha de referencia
- Hora de reset
- Duración del ciclo
- Orden de las actividades
- URLs de la Wiki
- Localizaciones
- Recompensas
- Objetos necesarios

Esto permite generar los embeds sin depender de una consulta a la Wiki en
cada ejecución.

---

# Datos adicionales de Zaishen

Las actividades Zaishen utilizan:

```text
data/source/zaishen_data.csv
```

Este CSV contiene información adicional para enriquecer las actividades,
incluyendo la URL de la Wiki y las recompensas en Zaishen Coins.

El proceso es:

```text
Rotación JSON
      │
      ▼
Actividad del día
      │
      ▼
zaishen_data.csv
      │
      ▼
Información enriquecida
      │
      ▼
Discord Embed
```

---

# Ejecución local

Para probar el bot manualmente:

```bash
python src/main.py
```

Esto permite comprobar el resultado antes de utilizar la ejecución automática
de GitHub Actions.

Para que funcione localmente, asegúrate de que `DISCORD_WEBHOOK_URL` esté
disponible como variable de entorno.

---

# GitHub Actions

GitHub Actions se utiliza como sistema de cron para ejecutar el bot
automáticamente.

El workflow obtiene la URL del webhook mediante el secret:

```text
DISCORD_WEBHOOK_URL
```

La URL del webhook nunca debe almacenarse directamente en el repositorio.

---

# Estructura del proyecto

Una versión simplificada del proyecto:

```text
gw_zaishen_activities_report/
│
├── .github/
│   └── workflows/
│       └── ...
│
├── data/
│   └── source/
│       ├── zaishen_data.csv
│       ├── zaishen_bounty.json
│       ├── zaishen_combat.json
│       ├── zaishen_missions.json
│       ├── zaishen_vanquish.json
│       ├── vanguard_quest.json
│       ├── shining_blade.json
│       └── nicholas_sandford.json
│
├── src/
│   ├── main.py
│   ├── daily_activities_embed.py
│   ├── zaishen_rotation.py
│   └── discord_client.py
│
├── config.yaml
└── README.md
```

---

# Próximos pasos

## Actividades semanales

Añadir las actividades semanales de Guild Wars 1 utilizando una arquitectura
similar a la de las diarias.

La intención es mantener la lógica de las semanales separada de la generación
del embed de las diarias.

## Eventos de Discord

Crear eventos programados de Discord para determinadas actividades de Guild
Wars 1.

Esto permitiría que el bot no solo informe de las actividades, sino que
también facilite organizar grupos para realizarlas.

## Precios de objetos de mazmorras

Añadir información sobre los precios de mercado de los objetos que se pueden
obtener en las mazmorras.

El objetivo sería mostrar información como:

```text
Mazmorra
 ├── Objetos obtenibles
 ├── Información de drop
 └── Precios actuales
```

De esta forma se podría identificar rápidamente qué mazmorras pueden resultar
más interesantes económicamente.

---

# License / Licencia

This project is a community-made tool for Guild Wars 1.

Guild Wars and all related assets are property of their respective owners.

Este proyecto es una herramienta creada por la comunidad para Guild Wars 1.

Guild Wars y todos los recursos relacionados son propiedad de sus respectivos
dueños.
