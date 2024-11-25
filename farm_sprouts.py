{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOhzXTon5vOMMPET+0X9jQp",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/tkhalid00/Sprouts-Farm-ERP/blob/main/Farm_Sprouts.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Step 0: Setup Environment\n",
        "\n",
        "# Install required modules\n",
        "# pandas and matplotlib need to be installed, while sqlite3 is included with Python.\n",
        "!pip install pandas matplotlib\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "wugLPo5KC9CW",
        "outputId": "7bb26f44-cd77-454a-9277-05a16a99d0e4"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: pandas in /usr/local/lib/python3.10/dist-packages (2.2.2)\n",
            "Requirement already satisfied: matplotlib in /usr/local/lib/python3.10/dist-packages (3.8.0)\n",
            "Requirement already satisfied: numpy>=1.22.4 in /usr/local/lib/python3.10/dist-packages (from pandas) (1.26.4)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.10/dist-packages (from pandas) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.10/dist-packages (from pandas) (2024.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.10/dist-packages (from pandas) (2024.2)\n",
            "Requirement already satisfied: contourpy>=1.0.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib) (1.3.1)\n",
            "Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.10/dist-packages (from matplotlib) (0.12.1)\n",
            "Requirement already satisfied: fonttools>=4.22.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib) (4.55.0)\n",
            "Requirement already satisfied: kiwisolver>=1.0.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib) (1.4.7)\n",
            "Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib) (24.2)\n",
            "Requirement already satisfied: pillow>=6.2.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib) (11.0.0)\n",
            "Requirement already satisfied: pyparsing>=2.3.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib) (3.2.0)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil>=2.8.2->pandas) (1.16.0)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Step 1: Environment Setup\n",
        "import pandas as pd\n",
        "import sqlite3\n",
        "from datetime import datetime\n",
        "\n",
        "# Establish connection\n",
        "conn = sqlite3.connect('farm_erp.db')\n",
        "cursor = conn.cursor()\n"
      ],
      "metadata": {
        "id": "VW_Gzn2ZdpHr"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Step 2: Database Initialization\n",
        "\n",
        "# Create tables for crops, production, sales, resources, and expenses\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS Crops (\n",
        "    CropID INTEGER PRIMARY KEY,\n",
        "    Name TEXT,\n",
        "    Season TEXT,\n",
        "    Acreage REAL\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS Production (\n",
        "    EntryID INTEGER PRIMARY KEY,\n",
        "    CropID INTEGER,\n",
        "    Date TEXT,\n",
        "    Quantity REAL,\n",
        "    Grade TEXT,\n",
        "    FOREIGN KEY(CropID) REFERENCES Crops(CropID)\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS Sales (\n",
        "    SaleID INTEGER PRIMARY KEY,\n",
        "    CropID INTEGER,\n",
        "    Quantity REAL,\n",
        "    Price REAL,\n",
        "    Buyer TEXT,\n",
        "    FOREIGN KEY(CropID) REFERENCES Crops(CropID)\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS Resources (\n",
        "    ResourceID INTEGER PRIMARY KEY,\n",
        "    Name TEXT,\n",
        "    Type TEXT,\n",
        "    Stock REAL\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS Expenses (\n",
        "    ExpenseID INTEGER PRIMARY KEY,\n",
        "    Date TEXT,\n",
        "    Category TEXT,\n",
        "    Description TEXT,\n",
        "    Amount REAL\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "conn.commit()\n",
        "print(\"Database initialized.\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "2p4cVKNvCD9-",
        "outputId": "2e48959e-2d48-4ffb-a413-ff661f8d2f8d"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Database initialized.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Step 3: CRUD Operations\n",
        "\n",
        "# Add crop\n",
        "def add_crop(name, season, acreage):\n",
        "    cursor.execute(\"INSERT INTO Crops (Name, Season, Acreage) VALUES (?, ?, ?)\", (name, season, acreage))\n",
        "    conn.commit()\n",
        "\n",
        "# View crops\n",
        "def view_crops():\n",
        "    return pd.read_sql_query(\"SELECT * FROM Crops\", conn)\n",
        "\n",
        "# Record production\n",
        "def record_production(crop_id, date, quantity, grade):\n",
        "    cursor.execute(\"INSERT INTO Production (CropID, Date, Quantity, Grade) VALUES (?, ?, ?, ?)\",\n",
        "                   (crop_id, date, quantity, grade))\n",
        "    conn.commit()\n",
        "\n",
        "# View production\n",
        "def view_production():\n",
        "    return pd.read_sql_query(\"SELECT * FROM Production\", conn)\n",
        "\n",
        "# Record sale\n",
        "def record_sale(crop_id, quantity, price, buyer):\n",
        "    cursor.execute(\"INSERT INTO Sales (CropID, Quantity, Price, Buyer) VALUES (?, ?, ?, ?)\",\n",
        "                   (crop_id, quantity, price, buyer))\n",
        "    conn.commit()\n",
        "\n",
        "# View sales\n",
        "def view_sales():\n",
        "    return pd.read_sql_query(\"SELECT * FROM Sales\", conn)\n"
      ],
      "metadata": {
        "id": "faCJSkWqd062"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Step 4: Reporting\n",
        "\n",
        "# Yield report\n",
        "def yield_report():\n",
        "    return pd.read_sql_query(\"\"\"\n",
        "    SELECT Crops.Name, SUM(Production.Quantity) AS TotalYield, Production.Grade\n",
        "    FROM Production\n",
        "    JOIN Crops ON Production.CropID = Crops.CropID\n",
        "    GROUP BY Crops.Name, Production.Grade\n",
        "    \"\"\", conn)\n",
        "\n",
        "# Profitability report\n",
        "def profitability_report():\n",
        "    return pd.read_sql_query(\"\"\"\n",
        "    SELECT Crops.Name, SUM(Sales.Price * Sales.Quantity) AS Revenue,\n",
        "           (SELECT SUM(Amount) FROM Expenses WHERE Category = 'Crop') AS Expenses\n",
        "    FROM Sales\n",
        "    JOIN Crops ON Sales.CropID = Crops.CropID\n",
        "    GROUP BY Crops.Name\n",
        "    \"\"\", conn)\n"
      ],
      "metadata": {
        "id": "HgQeWmrod6LB"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Step 5: Testing and Visualization\n",
        "\n",
        "# Drop the existing Production and Sales tables if they exist\n",
        "cursor.execute(\"DROP TABLE IF EXISTS Production\")\n",
        "cursor.execute(\"DROP TABLE IF EXISTS Sales\")\n",
        "\n",
        "# Recreate the Production table with the correct schema\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS Production (\n",
        "    EntryID INTEGER PRIMARY KEY,\n",
        "    CropID INTEGER,\n",
        "    Date TEXT,\n",
        "    Quantity REAL,\n",
        "    Grade TEXT,\n",
        "    FOREIGN KEY(CropID) REFERENCES Crops(CropID)\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "# Recreate the Sales table with the correct schema\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS Sales (\n",
        "    SaleID INTEGER PRIMARY KEY,\n",
        "    CropID INTEGER,\n",
        "    Quantity REAL,\n",
        "    Price REAL,\n",
        "    Buyer TEXT,\n",
        "    FOREIGN KEY(CropID) REFERENCES Crops(CropID)\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "conn.commit()\n",
        "print(\"Production and Sales tables recreated with the correct schema.\")\n",
        "\n",
        "# Add sample crops\n",
        "add_crop(\"Wheat\", \"Winter\", 50)\n",
        "add_crop(\"Corn\", \"Summer\", 30)\n",
        "\n",
        "# Record production\n",
        "record_production(1, \"2024-11-26\", 1000, \"A\")\n",
        "record_production(1, \"2024-11-27\", 200, \"B\")\n",
        "record_production(2, \"2024-11-26\", 800, \"A\")\n",
        "\n",
        "# Record sales\n",
        "record_sale(1, 500, 10.5, \"Local Market\")\n",
        "record_sale(2, 300, 12.0, \"Exporter\")\n",
        "\n",
        "# View data\n",
        "print(\"Crops:\\n\", view_crops())\n",
        "print(\"Production:\\n\", view_production())\n",
        "print(\"Sales:\\n\", view_sales())\n",
        "\n",
        "# Generate and visualize reports\n",
        "yield_df = yield_report()\n",
        "print(\"Yield Report:\\n\", yield_df)\n",
        "\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "# Plot yield report\n",
        "yield_df.plot(kind='bar', x='Name', y='TotalYield', title=\"Yield per Crop\")\n",
        "plt.show()\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 937
        },
        "id": "p8meRiw3d9Po",
        "outputId": "a7f64865-1d74-47f4-9710-324b47e0c43e"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Production and Sales tables recreated with the correct schema.\n",
            "Crops:\n",
            "    CropID   Name  Season  Acreage\n",
            "0       1  Wheat  Winter     50.0\n",
            "1       2   Corn  Summer     30.0\n",
            "2       3  Wheat  Winter     50.0\n",
            "3       4   Corn  Summer     30.0\n",
            "4       5  Wheat  Winter     50.0\n",
            "5       6   Corn  Summer     30.0\n",
            "6       7  Wheat  Winter     50.0\n",
            "7       8   Corn  Summer     30.0\n",
            "Production:\n",
            "    EntryID  CropID        Date  Quantity Grade\n",
            "0        1       1  2024-11-26    1000.0     A\n",
            "1        2       1  2024-11-27     200.0     B\n",
            "2        3       2  2024-11-26     800.0     A\n",
            "Sales:\n",
            "    SaleID  CropID  Quantity  Price         Buyer\n",
            "0       1       1     500.0   10.5  Local Market\n",
            "1       2       2     300.0   12.0      Exporter\n",
            "Yield Report:\n",
            "     Name  TotalYield Grade\n",
            "0   Corn       800.0     A\n",
            "1  Wheat      1000.0     A\n",
            "2  Wheat       200.0     B\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 640x480 with 1 Axes>"
            ],
            "image/png": "iVBORw0KGgoAAAANSUhEUgAAAjAAAAHmCAYAAABtfrTAAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguMCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy81sbWrAAAACXBIWXMAAA9hAAAPYQGoP6dpAAA0jElEQVR4nO3de1hVZf7//9fmjIcNnjglIhqmGGVqGeZZRvIw5uRM2ZB5Gm0MdNDJzKk0rTQdNUMtsk+TVjbVzGf0YzVh5qlUEg95PlaWTgbkECCYoLB+f/hzfduBpbVxc8PzcV37utz3fe+13ktu3S/WvtfaDsuyLAEAABjEy9MFAAAAXCkCDAAAMA4BBgAAGIcAAwAAjEOAAQAAxiHAAAAA4xBgAACAcQgwAADAOAQYAABgHAIMUIs1b95cw4cP/1mvdTgcevzxx39y3OOPPy6Hw/Gz9gEAl0KAAWqgvn37qkGDBsrJyanQV1BQoPDwcHXq1Enl5eUeqK76W7Fihfr27avGjRvLz89PERERuuuuu7Ru3TpPlwbg/+fj6QIAuN9zzz2n66+/XhMmTNDrr7/u0veXv/xFp06dUkZGhlq3bi0vL36PuciyLI0cOVJLly7VTTfdpIkTJyosLExff/21VqxYod69e2vz5s3q3Lmzp0sFaj0CDFADRUdHa9q0aZo8ebKGDx+uPn36SJK2bdum9PR0Pfjgg7rxxhs9XOXVV15ertLSUgUEBFTaP2/ePC1dulSpqamaP3++y0dfjzzyiF599VX5+Fz6v83i4mLVrVvX7XUDqIhfvYAaauLEibrhhhv0wAMP6OzZsyorK9Mf//hHRUVFadq0aZIqXwOTn5+v1NRURUZGyt/fX9dee61mz559WR83bdq0STfffLMCAgLUsmVLvfDCC5ddb48ePXT99ddrx44d6ty5swIDAxUdHa309PQKY0tKSjRt2jRde+218vf3V2RkpB566CGVlJS4jHM4HEpJSdHy5cvVtm1b+fv7KyMjo9L9f/fdd5o1a5Zat26tuXPnVrpuZ+jQobrlllskSUuXLpXD4dDGjRv1wAMPKCQkRE2bNrXHPvfcc/Y+IyIilJycrPz8/J99zABccQYGqKF8fHy0ZMkSde7cWU888YRCQkK0c+dOZWRkqE6dOpW+5syZM+revbu++uor3X///WrWrJm2bNmiKVOm6Ouvv9aCBQsuub+9e/eqT58+atKkiR5//HGdP39e06ZNU2ho6GXX/O2336pfv3666667dM899+itt97S2LFj5efnp5EjR0q6cBZl4MCB2rRpk8aMGaM2bdpo7969euaZZ3TkyBGtXLnSZZvr1q3TW2+9pZSUFDVu3FjNmzevdN+bNm1SXl6eUlNT5e3tfdk1P/DAA2rSpImmTp2q4uJiSRcWLk+fPl0JCQkaO3asDh8+rOeff17btm3T5s2b5evre0XHDKASFoAaLSUlxfL19bXq1atn3XPPPS59UVFR1rBhw+znTzzxhFW3bl3ryJEjLuMefvhhy9vb2zp+/LjdJsmaNm2a/XzQoEFWQECA9eWXX9ptBw4csLy9va3L+a+me/fuliRr3rx5dltJSYnVrl07KyQkxCotLbUsy7JeffVVy8vLy/roo49cXp+enm5JsjZv3uxSo5eXl7V///6f3P+zzz5rSbJWrFjxk2Mty7JefvllS5LVpUsX6/z583Z7bm6u5efnZ/Xp08cqKyuz2xctWmRJsv72t79d8TEDqIiPkIAa7qmnnlKjRo3k5eWlZ5555kfH/uMf/1DXrl3VoEEDnTp1yn4kJCSorKxMH374YaWvKysr0+rVqzVo0CA1a9bMbm/Tpo0SExMvu1YfHx/df//99nM/Pz/df//9ys3N1Y4dO+wa27Rpo9atW7vU2KtXL0nS+vXrXbbZvXt3xcbG/uS+CwsLJUn169e/7HolafTo0S5nbD744AOVlpYqNTXVZYH06NGj5XQ69e67717xMQOoiI+QgBrO6XTquuuu06lTp37y45yjR49qz549atKkSaX9ubm5lbZ/8803+u677xQTE1Oh77rrrtO///3vy6o1IiKiwiLYVq1aSZK++OIL3XrrrTp69KgOHjx42TVGR0df1r6dTqck6fTp05c1/lLb//LLLyVdOO7v8/PzU4sWLez+iy7nmAFURIABYCsvL9evfvUrPfTQQ5X2X3xj9aTy8nLFxcVp/vz5lfZHRka6PA8MDLys7bZu3VrShbU8gwYNuux6Lnf7ANyLAAPA1rJlSxUVFSkhIeGKXtekSRMFBgbq6NGjFfoOHz582ds5efJkhUuRjxw5Ikn24tuWLVtq9+7d6t27t1vv8NulSxc1aNBAf//73/WXv/zlihbyfl9UVJSkC8fdokULu720tFTHjh2r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27dvJ8DA444dOybLstSiRQtlZWWpSZMmdp+fn59CQkLk7e3twQpRGzEvqwcCDCro37+/Jk2apAMHDiguLk6+vr4u/QMHDvRQZahtoqKiJKnCQnLAk5iX1QMfIaECL69LX13vcDhUVlZ2FasB/p8DBw7o+PHjKi0tdWknVMOTmJeeQYABUO19/vnn+s1vfqO9e/fK4XDY6w4urkMgVMMTmJeexY3s4OLcuXPy8fHRvn37PF0KYPvTn/6k6Oho5ebmqk6dOtq/f78+/PBDdezYURs2bPB0eailmJeexRoYuPD19VWzZs34zQHVSmZmptatW6fGjRvLy8tLXl5e6tKli2bNmqXx48frk08+8XSJqIWYl57FGRhU8Mgjj+gvf/kLN6xDtVFWVqb69etLkho3bqyTJ09KurCY8vDhw54sDbUY89KzOAODChYtWqRPP/1UERERioqKUt26dV36d+7c6aHKUFtdf/312r17t6Kjo9WpUyfNmTNHfn5+WrJkCZf7w2OYl55FgEEFgwYN8nQJgItHH31UxcXFkqQZM2ZowIAB6tq1qxo1aqQ333zTw9WhtmJeehZXIQEwUl5enho0aODyXV2ApzEvrx4CDC5px44dOnjwoCSpbdu2uummmzxcEWq7Tz/9VJ999pm6deumwMBAWZbFGwU8jnnpGQQYVJCbm6shQ4Zow4YN9tfE5+fnq2fPnnrjjTdcbpsNXA3//e9/ddddd2n9+vVyOBw6evSoWrRooZEjR6pBgwaaN2+ep0tELcS89CyuQkIF48aN0+nTp7V//37l5eUpLy9P+/btU2FhocaPH+/p8lALTZgwQb6+vjp+/LjLN6TffffdysjI8GBlqM2Yl57FIl5UkJGRoQ8++EBt2rSx22JjY7V48WL16dPHg5Whtnr//fe1evVqNW3a1KU9JiZGX375pYeqQm3HvPQszsCggvLy8gpf4ChduMkdX14GTyguLnb5DfeivLw8+fv7e6AigHnpaQQYVNCrVy/96U9/sm/KJElfffWVJkyYoN69e3uwMtRWXbt21SuvvGI/dzgcKi8v15w5c9SzZ08PVobajHnpWSziRQUnTpzQwIEDtX//fkVGRtpt119/vVatWlXhdClQ1fbt26fevXurffv2WrdunT0/8/LytHnzZrVs2dLTJaIWYl56FgEGlbIsSx988IEOHTokSWrTpo0SEhI8XBVqs4KCAi1atEi7d+9WUVGR2rdvr+TkZIWHh3u6NNRizEvPIcDAtm7dOqWkpOjjjz+W0+l06SsoKFDnzp2Vnp6url27eqhCAAAuIMDANnDgQPXs2VMTJkyotD8tLU3r16/XihUrrnJlwIV7EWVlZSk3N7fCYvL77rvPQ1WhtmNeeg4BBraoqChlZGS4XD79fYcOHVKfPn10/Pjxq1wZaru3335bSUlJKioqktPpdLnLqcPh4JvT4RHMS88iwMAWEBCgffv26dprr620/9NPP1VcXJy+++67q1wZartWrVqpX79+mjlzZqWXrQKewLz0LC6jhu2aa67Rvn37Ltm/Z88eFqbBI7766iuNHz+eNwlUK8xLzyLAwNavXz899thjOnv2bIW+7777TtOmTdOAAQM8UBlqu8TERG3fvt3TZQAumJeexUdIsOXk5Kh9+/by9vZWSkqKrrvuOkkX1r4sXrxYZWVl2rlzp0JDQz1cKWqDVatW2X/+5ptvNGPGDI0YMUJxcXEV7hQ9cODAq10eainmZfVBgIGLL7/8UmPHjtXq1at1cWo4HA4lJiZq8eLFio6O9nCFqC28vC7vBLHD4VBZWVkVVwNcwLysPggwqNS3336rTz/9VJZlKSYmRg0aNPB0SaiFPv/8c7Vo0cLTZQAumJfVAwEGQLXl5eWlqKgo9erVSz179lTPnj11zTXXeLos1HLMy+qBAAOg2tqwYYP92Lp1q0pLS9WiRQuXNw7WZOFqY15WDwQYAEY4e/astmzZYr9xZGVl6dy5c2rdurX279/v6fJQSzEvPYcAA8AopaWl2rx5s9577z298MILKioqYrEkPI55efURYABUa6Wlpfr444+1fv16+5R9ZGSkunXrpm7duql79+5q1qyZp8tELcO89DwCDIBqq1evXtq6dauio6PVvXt3de3aVd27d+eO0PAo5mX1QIABUG35+voqPDxcgwYNUo8ePdS9e3c1atTI02WhlmNeVg8EGADVVnFxsT766CNt2LBB69ev165du9SqVSt1797dfuNo0qSJp8tELcO8rB4IMACMcfr0aW3atMled7B7927FxMT86JeQAlWNeekZfJkjAGPUrVtXDRs2VMOGDdWgQQP5+Pjo4MGDni4LtRzz0jM4AwOg2iovL9f27dvtU/WbN29WcXGxrrnmGvuGYT179lRUVJSnS0UtwrysHggwAKotp9Op4uJihYWF2W8KPXr0UMuWLT1dGmox5mX1QIABUG298MIL6tmzp1q1auXpUgAb87J6IMAAAADjsIgXAAAYhwADAACMQ4ABAADGIcAAAADjEGAAXDXDhw+Xw+HQ008/7dK+cuVKORwOD1UFwEQEGABXVUBAgGbPnq1vv/3W06UAMBgBBsBVlZCQoLCwMM2aNavS/v/+97+65557dM0116hOnTqKi4vT3//+d5cxPXr00Lhx45SamqoGDRooNDRUL774ooqLizVixAjVr19f1157rd577z2X1+3bt099+/ZVvXr1FBoaqqFDh+rUqVNVdqwAqg4BBsBV5e3trZkzZ2rhwoX6z3/+U6H/7Nmz6tChg959913t27dPY8aM0dChQ5WVleUybtmyZWrcuLGysrI0btw4jR07Vr/73e/UuXNn7dy5U3369NHQoUN15swZSVJ+fr569eqlm266Sdu3b1dGRoZycnJ01113XZXjBuBe3MgOwFUzfPhw5efna+XKlYqPj1dsbKxeeuklrVy5Ur/5zW90qf+OBgwYoNatW2vu3LmSLpyBKSsr00cffSRJKisrU1BQkO6880698sorkqTs7GyFh4crMzNTt956q5588kl99NFHWr16tb3d//znP4qMjNThw4e5qypgGB9PFwCgdpo9e7Z69eqlBx980KW9rKxMM2fO1FtvvaWvvvpKpaWlKikpUZ06dVzG3XDDDfafvb291ahRI8XFxdltoaGhkqTc3FxJ0u7du7V+/XrVq1evQi2fffYZAQYwDAEGgEd069ZNiYmJmjJlioYPH263//Wvf9Wzzz6rBQsWKC4uTnXr1lVqaqpKS0tdXu/r6+vy3OFwuLRdvKqpvLxcklRUVKRf//rXmj17doVawsPD3XVYAK4SAgwAj3n66afVrl07XXfddXbb5s2bdccdd+jee++VdCGAHDlyRLGxsb9oX+3bt9f//u//qnnz5vLx4b8+wHQs4gXgMXFxcUpKSlJaWprdFhMTozVr1mjLli06ePCg7r//fuXk5PzifSUnJysvL0/33HOPtm3bps8++0yrV6/WiBEjVFZW9ou3D+DqIsAA8KgZM2bYH/NI0qOPPqr27dsrMTFRPXr0UFhYmAYNGvSL9xMREaHNmzerrKxMffr0UVxcnFJTUxUcHCwvL/4rBEzDVUgAAMA4/NoBAACMQ4ABAADGIcAAAADjEGAAAIBxCDAAAMA4BBgAAGAcAgwAADAOAQYAABiHAAMAAIxDgAEAAMYhwAAAAOMQYAAAgHH+P2Vk9e8iQm5eAAAAAElFTkSuQmCC\n"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Code Deployment"
      ],
      "metadata": {
        "id": "KzfzVu3tganS"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "u74lhoR2eVbv",
        "outputId": "11bf1974-578d-49ac-8135-7d4adb46be98"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: streamlit in /usr/local/lib/python3.10/dist-packages (1.40.2)\n",
            "Requirement already satisfied: altair<6,>=4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.2.2)\n",
            "Requirement already satisfied: blinker<2,>=1.0.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (1.9.0)\n",
            "Requirement already satisfied: cachetools<6,>=4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (5.5.0)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (8.1.7)\n",
            "Requirement already satisfied: numpy<3,>=1.23 in /usr/local/lib/python3.10/dist-packages (from streamlit) (1.26.4)\n",
            "Requirement already satisfied: packaging<25,>=20 in /usr/local/lib/python3.10/dist-packages (from streamlit) (24.2)\n",
            "Requirement already satisfied: pandas<3,>=1.4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (2.2.2)\n",
            "Requirement already satisfied: pillow<12,>=7.1.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (11.0.0)\n",
            "Requirement already satisfied: protobuf<6,>=3.20 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.25.5)\n",
            "Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (17.0.0)\n",
            "Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.10/dist-packages (from streamlit) (2.32.3)\n",
            "Requirement already satisfied: rich<14,>=10.14.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (13.9.4)\n",
            "Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (9.0.0)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.10/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.3.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.12.2)\n",
            "Requirement already satisfied: watchdog<7,>=2.1.5 in /usr/local/lib/python3.10/dist-packages (from streamlit) (6.0.0)\n",
            "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.10/dist-packages (from streamlit) (3.1.43)\n",
            "Requirement already satisfied: pydeck<1,>=0.8.0b4 in /usr/local/lib/python3.10/dist-packages (from streamlit) (0.9.1)\n",
            "Requirement already satisfied: tornado<7,>=6.0.3 in /usr/local/lib/python3.10/dist-packages (from streamlit) (6.3.3)\n",
            "Requirement already satisfied: entrypoints in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (0.4)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (3.1.4)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (4.23.0)\n",
            "Requirement already satisfied: toolz in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (0.12.1)\n",
            "Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.10/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.11)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.10/dist-packages (from pandas<3,>=1.4.0->streamlit) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.10/dist-packages (from pandas<3,>=1.4.0->streamlit) (2024.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.10/dist-packages (from pandas<3,>=1.4.0->streamlit) (2024.2)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (3.4.0)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (2.2.3)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.27->streamlit) (2024.8.30)\n",
            "Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.10/dist-packages (from rich<14,>=10.14.0->streamlit) (3.0.0)\n",
            "Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.10/dist-packages (from rich<14,>=10.14.0->streamlit) (2.18.0)\n",
            "Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.10/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.1)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from jinja2->altair<6,>=4.0->streamlit) (3.0.2)\n",
            "Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (24.2.0)\n",
            "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2024.10.1)\n",
            "Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.35.1)\n",
            "Requirement already satisfied: rpds-py>=0.7.1 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.21.0)\n",
            "Requirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.10/dist-packages (from markdown-it-py>=2.2.0->rich<14,>=10.14.0->streamlit) (0.1.2)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.16.0)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Step 7: User Interface with Streamlit\n",
        "\n",
        "import streamlit as st\n",
        "import sqlite3\n",
        "\n",
        "# Connect to the database\n",
        "conn = sqlite3.connect('farm_erp.db')\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# Create a function to add crop\n",
        "def add_crop_to_db(name, grade, season, farm_number):\n",
        "    cursor.execute(\"INSERT INTO Crops (Name, Season, Acreage) VALUES (?, ?, ?)\", (name, season, farm_number))\n",
        "    conn.commit()\n",
        "\n",
        "# Streamlit UI\n",
        "st.title(\"Agricultural Farm ERP\")\n",
        "\n",
        "# Input form for crop details\n",
        "with st.form(key='crop_form'):\n",
        "    crop_name = st.text_input(\"Crop Name\")\n",
        "    crop_grade = st.text_input(\"Crop Grade\")\n",
        "    crop_season = st.selectbox(\"Season\", [\"Winter\", \"Summer\", \"Spring\", \"Fall\"])\n",
        "    farm_number = st.number_input(\"Farm Number\", min_value=1, step=1)\n",
        "\n",
        "    # Submit button\n",
        "    submit_button = st.form_submit_button(label='Add Crop')\n",
        "\n",
        "if submit_button:\n",
        "    if crop_name and crop_grade and crop_season:\n",
        "        # Add crop to database\n",
        "        add_crop_to_db(crop_name, crop_grade, crop_season, farm_number)\n",
        "        st.success(f\"Crop {crop_name} added successfully!\")\n",
        "    else:\n",
        "        st.error(\"Please fill all fields.\")\n",
        "\n",
        "# View existing crops\n",
        "st.subheader(\"Existing Crops\")\n",
        "crops_df = pd.read_sql_query(\"SELECT * FROM Crops\", conn)\n",
        "st.write(crops_df)\n"
      ],
      "metadata": {
        "id": "QTU4ozmigdPs",
        "outputId": "6c37bad8-f957-4cef-d61e-f74a48abedd6",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2024-11-25 22:47:19.089 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.093 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.098 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.099 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.103 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.104 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.107 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.108 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.110 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.111 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.112 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.114 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.115 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.116 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.117 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.119 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.120 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.121 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.123 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.124 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.125 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.130 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.131 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.132 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.133 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.138 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.139 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.140 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.141 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.143 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.144 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.146 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.147 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.149 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.150 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.217 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2024-11-25 22:47:19.219 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "No0oantlggAW"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}
