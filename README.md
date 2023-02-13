# UTU Chess Elo System

## The Plan
### Files:
- Have a text file for every **player** that contains:
    - Name
    - Current Elo
    - Game history
        - | **Time** (day/month/year) | **White_name** | **Black_name** | **White_Elo** | **Black_Elo** | **Result** (0.5-0.5, 1-0, 0-1) |
        - eg. | "15/02/2023" | Santeri Salomaa | Elias Ervelä | 1800 | 1200 | 0-1 |
    - Elo history
        - | Time | Elo |
- Have a file that contains **game history**:
    - | **Time** (day/month/year) | **White_name** | **Black_name** | **White_Elo** | **Black_Elo** | **Result** (0.5-0.5, 1-0, 0-1) |
- Have a file that contains current **Elo leaderboard** (in decending order)
    - | **Player** | **Elo** | 

### Methods:
