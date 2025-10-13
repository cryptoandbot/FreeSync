# SmartEdge – Betting Arbitrage Discord Bot

A Discord bot that scans sportsbook odds through the **OddsAPI**, detects **arbitrage opportunities**, and notifies users in real time.
It tracks major U.S. sports and helps users calculate optimal stake splits to guarantee profit regardless of the game outcome.

---

## Commands

* **$setChannel**
  Set the current text channel as the destination for arbitrage alerts.
  The bot will automatically start sending detected opportunities there.

* **$stake [total_stake]**
  Calculates how much to wager on each side of a detected arbitrage to guarantee a profit, based on the total stake you input.

---

## Features

* Fetches live odds via **OddsAPI**
* Detects **arbitrage** and **inefficient lines**
* Supports **major U.S. sports** only
* Calculates **stake allocation** for optimal profit
* Sends **real-time alerts** to your chosen Discord channel

---

## Tech Stack

* **Language:** Python
* **Framework:** `discord.py`
* **Data Source:** OddsAPI
* **Deployment:** Works on any server or VPS
