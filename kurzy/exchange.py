import httpx


CNB_URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/denni_kurz.txt"


def get_eur_rate():
    try:
        response = httpx.get(CNB_URL, timeout=10.0)
        response.raise_for_status()
    except httpx.RequestError as e:
        print(f"Chyba při připojení k ČNB: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Chyba HTTP odpovědi: {e}")
        return None

    lines = response.text.splitlines()

    for line in lines:
        parts = line.split("|")
        if len(parts) == 5 and parts[3] == "EUR":
            try:
                amount = int(parts[2])
                rate = float(parts[4].replace(",", "."))
                return rate / amount
            except ValueError:
                return None

    print("Kurz EUR nebyl nalezen.")
    return None


def get_amount():
    while True:
        user_input = input("Zadejte částku: ").strip().replace(",", ".")
        try:
            amount = float(user_input)
            if amount < 0:
                print("Částka musí být nezáporné číslo.")
                continue
            return amount
        except ValueError:
            print("Neplatná částka. Zadejte číslo.")


def get_direction():
    while True:
        print("Zvolte mněnu převodu:")
        print("1 - EUR -> CZK")
        print("2 - CZK -> EUR")
        choice = input("Vaše volba (1/2): ").strip()

        if choice == "1":
            return "EUR_CZK"
        elif choice == "2":
            return "CZK_EUR"
        else:
            print("Neplatná volba. Zadejte 1 nebo 2.")


def main():
    print("Načítám aktuální kurz EUR z ČNB...")
    rate = get_eur_rate()

    if rate is None:
        print("Program bude ukončen.")
        return

    print(f"Aktuální kurz EUR: 1 EUR = {rate:.3f} CZK")

    direction = get_direction()
    amount = get_amount()

    if direction == "EUR_CZK":
        result = amount * rate
        print(f"{amount:.2f} EUR = {result:.2f} CZK")
    else:
        result = amount / rate
        print(f"{amount:.2f} CZK = {result:.2f} EUR")


if __name__ == "__main__":
    main()
